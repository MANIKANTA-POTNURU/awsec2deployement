from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import generate_csv
from .views import upload_file, file_list, file_detail
urlpatterns = [
    path('',views.index,name="index"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('login',views.login,name="login"),
    path('registration',views.registration,name="registration"),
    path("SignUpDatafunction",views.SignUpDatafunction,name="SignUpDatafunction"),
    path("checkuserlogin",views.checkuserlogin,name="checkuserlogin"),
    path('userhome',views.userhome,name="userhome"),
    path('userchangepwd',views.userchangepwd,name="userchangepwd"),
    path('userupdatepwd', views.userupdatepwd, name="userupdatepwd"),
    path('viewusers', views.viewusers, name="viewusers"),
    path('viewprofile', views.viewprofile, name="viewprofile"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('viewproducts', views.viewproducts, name="viewproducts"),
    path("deleteproduct/<int:uid>", views.deleteproduct, name="deleteproduct"),

    path("category/<str:id>",views.category,name="category"),

    path('addcartfun', views.add_cart, name="addcartfun"),
    path('cart/',views.getcart,name="getcart"),

    path('checkout', views.checkout, name="checkout"),

    path('generate-csv/', generate_csv, name='generate-csv'),

    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('files/<int:file_id>/', file_detail, name='file_detail'),

    path('viewproduct/<int:product_id>/', views.viewproduct, name='viewproduct'),

    path('logout', views.logout, name="logout"),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)