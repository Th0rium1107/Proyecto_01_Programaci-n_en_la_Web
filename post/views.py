from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, ContactoForm
from django.contrib.auth.models import User  # Importa el modelo User
from .models import Post, InfoContacto # Importa el modelo post
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import RegistroForm
from django.contrib import messages

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'post/registro.html', {'form': form})

from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-created_at')  # o solo disponibles si prefieres
    return render(request, 'post/index.html', {'posts': posts})

@login_required
def categorias(request):
    return render(request, 'post/categorias.html')

@login_required
def mis_publicaciones(request):
    # Filtramos solo los posts creados por el usuario actual
    publicaciones = Post.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'post/mis_publicaciones.html', {
        'publicaciones': publicaciones
    })

@login_required
def perfil(request):
    # Intentamos obtener la información de contacto del usuario, si existe
    info_contacto = InfoContacto.objects.filter(usuario=request.user).first()
    return render(request, 'post/perfil_usuario.html', {'info_contacto': info_contacto})

@login_required
def agregar_comentario(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('detalle_post', post_id=post.id)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    return redirect('detalle_post', post_id=comment.post.id)

@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.dislikes += 1
    comment.save()
    return redirect('detalle_post', post_id=comment.post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return redirect('detalle_post', post_id=post.id)


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes += 1
    post.save()
    return redirect('detalle_post', post_id=post.id)

@login_required
def eliminar_comentario(request, comment_id):
    comentario = get_object_or_404(Comment, id=comment_id)

    # Verifica que sea el autor o un superusuario
    if comentario.author == request.user or request.user.is_superuser:
        comentario.delete()
        messages.success(request, "Comentario eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este comentario.")

    # Redirige de nuevo al detalle del post
    return redirect('detalle_post', post_id=comentario.post.id)


def detalle_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comentarios = post.comments.all().order_by('-created_at')
    # Buscar la información de contacto del autor
    info_contacto = InfoContacto.objects.filter(usuario=post.author).first()
    return render(request, 'post/detalle_post.html', {'post': post, 'comentarios': comentarios, 'info_contacto': info_contacto})


#CRUD de publicaciones
def publicaciones(request):
    posts = Post.objects.filter(is_available=True, published=True).order_by('-created_at')
    return render(request, 'post/publicaciones.html', {'posts': posts})

@login_required
def nueva_publicacion(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Agrega request.FILES
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('publicaciones')
    else:
        form = PostForm()
    return render(request, 'post/nueva_publicacion.html', {'form': form})

@login_required
def editar_publicacion(request, post_id):   
    post = Post.objects.get(id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return redirect('publicaciones')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # Agrega request.FILES
        if form.is_valid():
            form.save()
            return redirect('publicaciones')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/editar_publicacion.html', {'form': form})

@login_required
def eliminar_publicacion(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return redirect('publicaciones')  # no tiene permiso
    if request.method == 'POST':
        post.delete()
        return redirect('publicaciones')
    return render(request, 'post/borrar_publicacion.html', {'post': post})

@login_required
def agregar_info(request):
    """Permite agregar información de contacto al usuario."""
    try:
        # Verificamos si ya tiene información de contacto
        contacto = request.user.infocontacto
        # Si ya existe, redirigimos directamente a la vista de editar
        return redirect('editar_info_contacto')
    except InfoContacto.DoesNotExist:
        contacto = None

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.usuario = request.user
            contacto.save()
            return redirect('perfil')
    else:
        form = ContactoForm()

    return render(request, 'post/agregar_info_contacto.html', {'form': form})


@login_required
def editar_info(request):
    """Permite editar la información de contacto existente."""
    contacto = get_object_or_404(InfoContacto, usuario=request.user)

    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ContactoForm(instance=contacto)

    return render(request, 'post/editar_info_contacto.html', {'form': form})
