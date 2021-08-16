from django.db.models import fields
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db.models import Q
from Social.models import Posts, Profile, Comment
from django.views import View
from Social.forms import PostForm, CommentForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView



class LandingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'social/landing.html')

class PostList(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        posts = Posts.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'posts' : posts, 
            'form' : form
        }

        return render(request, 'social/home.html', context)

class AddPost(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        form = PostForm()

        context = {
            'form' : form
        }

        return render(request, 'social/addpost.html', context)
    
    def post(self, request, *args, **kwargs):
        posts = Posts.objects.all().order_by('-created_on')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()


        context = {
            'posts' : posts,
            'form' : form
        }


        return redirect('post_list')


class SinglePost(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        posts = Posts.objects.get(pk = pk)
        form = CommentForm()

        comment = Comment.objects.filter(post = posts).order_by('-created_on')

        context = {
            'posts' : posts,
            'form' : form,
            'comment' : comment
            
        }


        return render(request, 'social/single_post.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Posts.objects.get(pk = pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()


        comment = Comment.objects.filter(post = post).order_by('-created_on')


        context = {
            'post' : post,
            'form' : form,
            'comment' : comment
        }

        return render(request, 'social/single_post.html', context)


class ProfileView(LoginRequiredMixin, View):
    def get(self,request,pk,  *args, **kwargs):
        profile = Profile.objects.get(pk = pk)
        user = profile.user
        post = Posts.objects.filter(author = user).order_by('-created_on')

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break

            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'profile' : profile,
            'user' : user,
            'post' : post,
            'number_of_followers' : number_of_followers,
            'is_following' : is_following
        }

        return render(request, 'social/profile.html', context)

class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['name', 'profile_picture', 'bio', 'location']
    template_name = 'social/profile_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs = {'pk' : pk})

class PostEdit( UpdateView):
    model = Posts
    fields = ['title', 'body', 'image']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('single_post', kwargs = {'pk' : pk})


class PostDelete(UserPassesTestMixin,LoginRequiredMixin, DeleteView):
    model = Posts
    template_name= 'social/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return  self.request.user == post.author

class DeleteComment(DeleteView):
    model = Comment
    template_name = 'social/delete_comment.html'
    success_url = reverse_lazy('post_list')

class Addfollower( View):
    def post(self, request, pk ,*args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveFollower( View):

    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk =pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk =profile.pk)


class AddLike(View, LoginRequiredMixin):
    def post(self, request, pk, *args, **kwargs):
        post = Posts.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if is_dislike:
            post.dislikes.remove(request.user)
        

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        
        return redirect('post_list')


class Dislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        post = Posts.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)


        

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)


        next = request.POST.get('next', '/')

        return redirect('post_list')



class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = Profile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list' : profile_list
        }

        return render(request, 'social/search.html', context)
