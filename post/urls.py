from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('categorias/', views.categorias, name='categorias'),

    path('publicaciones/', views.publicaciones, name='publicaciones'),

    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),


    path('perfil', views.perfil, name='perfil'),
    
    path('agregar_info/', views.agregar_info, name='agregar_info'),
    path('editar_info/', views.editar_info, name='editar_info'),

    #CRUD de publicaciones
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('publicaciones/nueva/', views.nueva_publicacion, name='nueva_publicacion'),
    path('publicaciones/editar/<int:post_id>/', views.editar_publicacion, name='editar_publicacion'),
    path('publicaciones/eliminar/<int:post_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),


    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),

    path('post/<int:post_id>/comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('comentario/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comentario/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),
    path('comentario/<int:comment_id>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),

    path('agregar-info/', views.agregar_info, name='agregar_info'),
]