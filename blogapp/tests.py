from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post,Comment

# Create your tests here.

#Class for Unit Tests

class BlogAPIUnitTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='testuser@gmail.com',password='testpassword')
        self.token = self.get_token_for_user(self.user)
        self.post = Post.objects.create(title='Test Post',content='This is a test post.',author=self.user)
        self.comment = Comment.objects.create(content='This is a test comment',post=self.post,author=self.user)
        self.register_url = reverse('register_user')
        self.login_url = reverse('login_user')
        self.posts_url = reverse('post_list_create')
        self.post_detail_url = reverse('post_list_update_delete',kwargs={'pk':self.post.id})
        self.comments_url = reverse('comment_list_create')
        self.comment_detail_url = reverse('comment_list_update_delete',kwargs={'pk':self.comment.id})

    def get_token_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }

    #Unit Test Case for Registration
    def test_registration(self):
        
        data = {
            'username' : 'newuser',
            'email' : 'newuser@example.com',
            'password' : 'newpassword'
        }
        response = self.client.post(self.register_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    #Unit Test Case for Login
    def test_login(self):
        
        data = {
            'username' : 'testuser',
            'password' : 'testpassword'
        }
        response = self.client.post(self.login_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)

    #Unit Test Case for Reading all Posts
    def test_read_all_posts(self):

        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    #Unit Test Case for Creating a post with authentications
    def test_create_post(self):
        
        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)
        data = {
            'title' : 'New Post',
            'content' : 'This is a new post.',
            'author' : self.user.id
        }
        response = self.client.post(self.posts_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    #Unit Test Case for Reading a single post
    def test_read_single_post(self):
        
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['id'],self.post.id)
        self.assertEqual(response.data['title'],self.post.title)
        self.assertEqual(response.data['content'],self.post.content)

    #Unit Test Case for Updating a post with authentications
    def test_update_post(self):
        
        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

        data = {
            'title':'Updated Post',
            'content':'This is an updated post',
            'author':self.user.id
        }

        response = self.client.put(self.post_detail_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Unit Test Case for Deleting a post
    def test_delete_post(self):

        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    #Unit Test Case for Reading comments related to a particular post with post_id
    def test_read_comment_for_post(self):

        response = self.client.get(self.comments_url,{'post_id':self.post.id},format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    #Unit Test Case for Reading single comment
    def test_read_single_comment(self):

        response = self.client.get(self.comment_detail_url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['id'],self.comment.id)
        self.assertEqual(response.data['content'],self.comment.content)
        self.assertEqual(response.data['post'],self.post.id)

    #Unit Test Case for Creating a comment with authentications
    def test_create_comment(self):

        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        
        data = {
            'content' : 'New comment.',
            'post' : self.post.id,
            'author' : self.user.id
        }

        response = self.client.post(self.comments_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    #Unit Test Case for updating a comment with authentications 
    def test_update_comment(self):

        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        
        data = {
            'content':'Updated Comment',
            'post' : self.post.id,
            'author':self.user.id
        }

        response = self.client.put(self.comment_detail_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Unit Test Case for deleting a comment with authentications
    def test_delete_comment(self):

        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)
        
        response = self.client.delete(self.comment_detail_url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        

#Class for Integration Tests

class BlogAPIIntegrationTestCase(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser',password='testpassword')
        self.post = Post.objects.create(title='Test Post',content='This is a test post.',author=self.user)
        self.posts_url = reverse('post_list_create')
        self.post_detail_url = reverse('post_list_update_delete',args=[self.post.id])
        self.comments_url = reverse('comment_list_create')

    def get_token_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }

    #Integration Test Case for registering and loging in new users
    def test_user_registration_and_login(self):
        # Register a new user
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Login with the same user
        login_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)

    #Integration Test Case for checking the relation between posts and comments
    def test_create_post_and_add_comment(self):
        # Create a post
        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        post_data = {
            'title': 'Integration Test Post',
            'content': 'This is a post created during an integration test.',
            'author' : self.user.id
        }
        response = self.client.post(self.posts_url, data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.data['id']

        # Add comment to the post
        comment_data = {
            'content' : 'This is a test comment',
            'post' : post_id,
            'author' : self.user.id
        }
        response = self.client.post(self.comments_url,data=comment_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        response = self.client.get(reverse('post_list_update_delete',args=[post_id]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('Integration Test Post',response.data['title'])

    #Integration Test Case for adding multiple comments to a post
    def test_post_with_multi_comments(self):
        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        comment_data_1 = {
            'content': 'First comment on the post',
            'post': self.post.id,
            'author' : self.user.id
        }

        comment_data_2 = {
            'content': 'Second comment on the post',
            'post': self.post.id,
            'author' : self.user.id
        }
        self.client.post(self.comments_url, data=comment_data_1)
        self.client.post(self.comments_url,data=comment_data_2)

        # Verify comments are correctly associated with the post
        response = self.client.get(self.post_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Integration Test Case for deleting posts and also comments associated with that post
    def test_post_delete_cascade_comments(self):
        token = self.get_token_for_user(self.user)['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ token)

        comment_data = {
            'content' : 'This is a comment to be deleted',
            'post' : self.post.id,
            'author' : self.user.id
        }
        response = self.client.post(self.comments_url,data=comment_data)
        comment_id = response.data['id']

        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('comment_list_update_delete',args=[comment_id]))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    #Integration Test Case for checking to create a post with unauthorized users
    def test_unauthenticated_create_post(self):
        # Attempt to create a post without authentication
        post_data = {
            'title': 'Unauthenticated Post',
            'content': 'This post should not be created without authentication.'
        }
        response = self.client.post(self.posts_url, data=post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

