from django.db import models
#Importante para poder referencial emodelo de auth_user
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modelo de la tabla Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Modelo de la tabla Post
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model): 
    title = models.CharField(max_length=200) 
    content = models.TextField() 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_healthy = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    published = models.BooleanField(default=True) 
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self): 
        return self.title

#Modelo de la tabla Comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comentario de {self.author.username} en {self.post.title}"

class InfoContacto(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    red_social = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Contacto de {self.usuario.username}"