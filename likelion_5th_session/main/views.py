from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment, Tag
from django.utils import timezone

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    if request.method == 'GET':
        comments = Comment.objects.filter(blog = blog)
        return render(request, 'main/detail.html', {
            'blog':blog,
            'comments':comments
        })
    elif request.method == 'POST':
        new_comment = Comment()

        new_comment.blog = blog
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()

        words = new_comment.content.split(' ')
        tag_list=[]

        for word in words:
            if len(word)>0:
                if word[0] == "#":
                    tag_list.append(word[1:])

        for tag in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=tag)
            new_comment.tags.add(tag.id)

        return redirect('main:detail', id)
    
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('main:detail', comment.blog.id)

def mainpage(request):
    blogs = Blog.objects.all()
    return render(request, 'main/mainpage.html', {'blogs':blogs})

def secondpage(request):
    return render(request, 'main/secondpage.html')

def create(request):
    if request.user.is_authenticated:
        new_blog = Blog()
        new_blog.title = request.POST['title']
        new_blog.writer = request.user
        new_blog.pub_date = timezone.now()
        new_blog.body = request.POST['body']
        new_blog.image = request.FILES.get('image')

        new_blog.save()

        words = new_blog.body.split(' ')

        tag_list = []
        for word in words:
            if len(word)>0:
                if word[0] =='#':
                    tag_list.append(word[1:])
        
        for tag in tag_list:
            tag, boolean = Tag.objects.get_or_create(name=tag)
            new_blog.tags.add(tag.id)
        
        return redirect('main:detail', new_blog.id)
    else:
        return redirect('accounts:login')

def new(request):
    return render(request, 'main/new.html')

def edit(request, id):
    edit_blog = Blog.objects.get(id=id)
    return render(request, 'main/edit.html', {'blog':edit_blog})

def update(request, id):
    if request.user.is_authenticated:
        update_blog = Blog.objects.get(id=id)
        if request.user == update_blog.writer:
            update_blog.title = request.POST['title']
            update_blog.pub_date = timezone.now()
            update_blog.body = request.POST['body']

            update_blog.save()

            update_blog.tags.clear()
            words = update_blog.body.split(' ')
            tag_list = []

            for word in words:
                if len(word)>0:
                    if word[0] == "#":
                        tag_list.append(word[1:])
            
            for tag in tag_list:
                tag, boolean = Tag.objects.get_or_create(name=tag)
                update_blog.tags.add(tag.id)

            return redirect('main:detail', update_blog.id)
    return redirect('accounts:login')

def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('main:mainpage')

def tag_list(request):
    empty_tags = Tag.objects.filter(blogs = None, comments = None)
    empty_tags.delete()
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {
        'tags':tags,
    })

def tag_blogs(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    blogs = tag.blogs.all()
    comments = tag.comments.all()
    return render(request, 'main/tag_blogs.html',{
        'tag':tag,
        'blogs':blogs,
        'comments':comments,
    })

    

