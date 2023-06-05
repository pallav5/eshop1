from django.urls import path, re_path
from .views import *

app_name = "eshopapp"
urlpatterns=[
      

        path("admin-site/login/", AdminLoginView.as_view(), name="adminlogin"),
        path("admin-logout/", AdminLogoutView.as_view(), name="adminlogout"),
        path('admin-dashboard/', 
             AdminDashboardView.as_view(),
             name='admindashboard'),


     path('admin/organization/create/', AdminOrganizationCreateView.as_view(), name = 'adminorganizationcreate'),
     path('admin/organization/update/<int:pk>/', AdminOrganizationUpdateView.as_view(), name = 'adminorganizationupdate'),
     path('admin/organization/detail/<int:pk>/', AdminOrganizationDetailView.as_view(), name = 'adminorganizationdetail'),



         path('admin/product-category-create/',
         AdminProductCategoryCreateView.as_view(),
         name="adminproductcategorycreate"),   

          path('admin/product-category-list/',
         AdminProductCategoryListView.as_view(),
         name="adminproductcategorylist"),

      
        
        path('admin/product-category/<int:pk>/update/',
         AdminProductCategoryUpdateView.as_view(),
         name="adminproductcategoryupdate"),
        
        path('admin/product-category/<int:pk>/delete/',
         AdminProductCategoryDeleteView.as_view(),
         name="adminproductcategorydelete"),


        path('admin/product-create/',
         AdminProductCreateView.as_view(),
         name="adminproductcreate"),

        path('admin/product-list/',
         AdminProductListView.as_view(),
         name="adminproductlist"),

        path('admin/product/<int:pk>/detail/',
         AdminProductDetailView.as_view(),
         name="adminproductdetail"),
        
        path('admin/product/<int:pk>/update/',
         AdminProductUpdateView.as_view(),
         name="adminproductupdate"),
        
        path('admin/product/<int:pk>/delete/',
         AdminProductDeleteView.as_view(),
         name="adminproductdelete"),

        
          #Product Brands
         path('admin/product-brand-create/',
         AdminProductBrandCreateView.as_view(),
         name="adminproductbrandcreate"),   

          path('admin/product-brand-list/',
         AdminProductBrandListView.as_view(),
         name="adminproductbrandlist"),

              
        path('admin/product-brand/<int:pk>/update/',
         AdminProductBrandUpdateView.as_view(),
         name="adminproductbrandupdate"),
        
        path('admin/product-brand/<int:pk>/delete/',
         AdminProductBrandDeleteView.as_view(),
         name="adminproductbranddelete"),  


          #Product Colors
         path('admin/product-color-create/',
         AdminProductColorCreateView.as_view(),
         name="adminproductcolorcreate"),   

          path('admin/product-color-list/',
         AdminProductColorListView.as_view(),
         name="adminproductcolorlist"),

              
        path('admin/product-color/<int:pk>/update/',
         AdminProductColorUpdateView.as_view(),
         name="adminproductcolorupdate"),
        
        path('admin/product-color/<int:pk>/delete/',
         AdminProductColorDeleteView.as_view(),
         name="adminproductcolordelete"),


         #Product Size
         path('admin/product-size-create/',
         AdminProductSizeCreateView.as_view(),
         name="adminproductsizecreate"),   

          path('admin/product-size-list/',
         AdminProductSizeListView.as_view(),
         name="adminproductsizelist"),

              
        path('admin/product-size/<int:pk>/update/',
         AdminProductSizeUpdateView.as_view(),
         name="adminproductsizeupdate"),
        
        path('admin/product-size/<int:pk>/delete/',
         AdminProductSizeDeleteView.as_view(),
         name="adminproductsizedelete"),  

        path('admin/orders/',
         AdminOrdersListView.as_view(),
         name="adminorders"),  
        path('admin/orders-detail/<int:pk>',
         AdminOrderDetailView.as_view(),
         name="adminorderdetail"),  
          path('admin/order/<int:pk>/delete/',
         AdminOrderDeleteView.as_view(),
         name="adminorderdelete"),  


         path('ajax-productstatus/change/',
         AjaxProductStatusChangeView.as_view(),
         name='ajax_product_statuschange'),   

         path('ajax-orderstatus/change/',
         AjaxOrderStatusChangeView.as_view(),
         name='ajax_order_statuschange'),   

          path('admin/image-slider/add/', SliderCreateView.as_view(), name = 'adminislidercreate'),
          path('admin/image-slider/list/', SliderListView.as_view(), name = 'adminsliderlist'),
          path('admin/image-slider/<int:pk>/detail/', SliderDetailView.as_view(), name = 'adminsliderdetail'),
          path('admin/image-slider/<int:pk>/update/', AdminSliderUpdateView.as_view(), name = 'adminsliderupdate'),
          # path('admin/image-slider/<int:pk>/delete/', AdminSliderDeleteView.as_view(), name = 'adminsliderdelete'),




     #Clients

      path('', ClientHomeView.as_view(),
              name='clienthome'),

      path('products/', ClientProductListView.as_view(),
              name='clientproductlist'),

      path('products/<str:str>/', ClientProductByMainCategoryListView.as_view(),
              name='clientproductbymaincategorylist'),
              
      path('product-category/<str:str>/', ClientProductByCategoryListView.as_view(),
              name='clientproductbycategorylist'),
              
      path('product/<slug:slug>/', ClientProductDetailView.as_view(),
      
              name='clientproductdetail'),

      path('product-search/result/', ClientProductSearchListView.as_view(),
      
              name='clientproductsearchlist'),

      path('customer-registration/', CustomerRegistrationView.as_view(),
      
              name='customerregistration'),

      path('customer-login/', CustomerLoginView.as_view(),
      
              name='customerlogin'),
      path('logout/', CustomerLogoutView.as_view(),
      
              name='customerlogout'),
         path("profile/", CustomerProfileView.as_view(), name="customerprofile"),  
          path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),   


        path("forgot-password/", PasswordForgotView.as_view(), name="passwordforgot"),
        path("password-reset/<email>/<token>/",
         PasswordResetView.as_view(), name="passwordreset"),  

        path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
        path("my-cart/", MyCartView.as_view(), name="mycart"),  
        path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),

        path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
      
           path("checkout/", CheckoutView.as_view(), name="checkout"),

       
]