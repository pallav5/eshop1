from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404
from django.db.models import Q
from .utils import password_reset_token
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = Organization.objects.first()

        return context

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return self.success_url




class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and Admin.objects.filter(user=request.user.id).exists():
            pass
        else:
            return redirect('/admin-site/login/?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['org'] = Organization.objects.first()
        context['orderlist'] = Order.objects.all().order_by('-id')
        
        
        return context   


class AdminLoginView(FormView):
    template_name = "admintemplates/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("eshopapp:admindashboard")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials "})
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return self.success_url
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['org'] = Organization.objects.first()

        
        return context 

class AdminLogoutView(AdminRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('eshopapp:adminlogin')

class AdminOrganizationCreateView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/organizationadd.html'
    # print(Organization.objects.all())
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy("eshopapp:admindashboard")



class AdminOrganizationUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/organizationadd.html'
    model = Organization
    form_class = OrganizationForm
 

    def get_success_url(self):

        return reverse_lazy('eshopapp:adminorganizationdetail', kwargs={'pk': self.kwargs['pk']})


class AdminOrganizationDetailView(AdminRequiredMixin,DetailView):
    template_name = 'admintemplates/organizationdetail.html'
    model = Organization


class AdminOrdersListView(AdminRequiredMixin,ListView):
    model = Order
    template_name = 'admintemplates/adminorderlist.html'
    
    
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset1 = Order.objects.all().order_by('-id')
        context['orderlist'] = queryset1
        return context
    

class AdminOrderDetailView(AdminRequiredMixin,DetailView):
    template_name = 'admintemplates/adminorderdetail.html'  
    model = Order
    context_object_name = 'adminorderdetail' 

class AdminOrderDeleteView(AdminRequiredMixin, DeleteView):

    model = Order
    success_url = reverse_lazy('eshopapp:adminorders')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Order deleted Successfully')
        return super(AdminOrderDeleteView,
                     self).delete(request, *args, **kwargs)


class AdminDashboardView(AdminRequiredMixin,TemplateView):
   
    template_name = 'admintemplates/admindashboard.html'

class AdminProductCategoryCreateView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminproductcategorycreate.html'  
    model = ProductCategory
    form_class = AdminProductCategoryCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcategorylist')


class AdminProductCategoryListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminproductcategorylist.html'  
    model = ProductCategory
    context_object_name = 'adminproductcategorylist' 
    
 
     
class AdminProductCategoryUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminproductcategorycreate.html'  
    model = ProductCategory
    form_class = AdminProductCategoryCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcategorylist')


class AdminProductCategoryDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminproductcategorycreate.html'
    model = ProductCategory
    success_url = reverse_lazy('eshopapp:adminproductcategorylist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Category deleted Successfully')
        return super(AdminProductCategoryDeleteView,
                     self).delete(request, *args, **kwargs)



class AdminProductCreateView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminproductcreate.html'  
    model = Product
    form_class = AdminProductCreateForm
    success_url = reverse_lazy('eshopapp:adminproductlist')

class AdminProductListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminproductlist.html'  
    model = Product
    context_object_name = 'adminproductlist'  
    paginate_by = 10 

class AdminProductDetailView(AdminRequiredMixin,DetailView):
    template_name = 'admintemplates/adminproductdetail.html'  
    model = Product
    context_object_name = 'adminproductdetail'  
     
class AdminProductUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminproductcreate.html'  
    model = Product
    form_class = AdminProductCreateForm
    success_url = reverse_lazy('eshopapp:adminproductlist')


class AdminProductDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminproductdelete.html'
    model = Product
    success_url = reverse_lazy('eshopapp:adminproductlist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted Successfully')
        return super(AdminProductDeleteView,
                     self).delete(request, *args, **kwargs)



#Brands
class AdminProductBrandCreateView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminproductbrandcreate.html'  
    model = ProductBrand
    form_class = AdminProductBrandCreateForm
    success_url = reverse_lazy('eshopapp:adminproductbrandlist')


class AdminProductBrandListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminproductbrandlist.html'  
    model = ProductBrand
    context_object_name = 'adminproductbrandlist' 

 
     
class AdminProductBrandUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminproductbrandcreate.html'  
    model = ProductBrand
    form_class = AdminProductBrandCreateForm
    success_url = reverse_lazy('eshopapp:adminproductbrandlist')


class AdminProductBrandDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminproductbrandcreate.html'
    model = ProductBrand
    success_url = reverse_lazy('eshopapp:adminproductbrandlist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Brand deleted Successfully')
        return super(AdminProductBrandDeleteView,
                     self).delete(request, *args, **kwargs)


#Colors
class AdminProductColorCreateView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminproductcolorcreate.html'  
    model = Color
    form_class = AdminProductColorCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')


class AdminProductColorListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminproductcolorlist.html'  
    model = Color
    context_object_name = 'adminproductcolorlist' 

 
     
class AdminProductColorUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/adminproductcolorcreate.html'  
    model = Color
    form_class = AdminProductColorCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')


class AdminProductColorDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminproductcolorcreate.html'
    model = Color
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Brand deleted Successfully')
        return super(AdminProductColorDeleteView,
                     self).delete(request, *args, **kwargs)


#Size
class AdminProductColorCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admintemplates/adminproductcolorcreate.html'  
    model = Color
    form_class = AdminProductColorCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')


class AdminProductColorListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminproductcolorlist.html'  
    model = Color
    context_object_name = 'adminproductcolorlist' 
    

 
     
class AdminProductColorUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminproductcolorcreate.html'  
    model = Color
    form_class = AdminProductColorCreateForm
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')


class AdminProductColorDeleteView(AdminRequiredMixin,  DeleteView):
    template_name = 'admintemplates/adminproductcolorcreate.html'
    model = Color
    success_url = reverse_lazy('eshopapp:adminproductcolorlist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Color deleted Successfully')
        return super(AdminProductColorDeleteView,
                     self).delete(request, *args, **kwargs)
    
#Size    

class AdminProductSizeCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admintemplates/adminproductsizecreate.html'  
    model = Size
    form_class = AdminProductSizeCreateForm
    success_url = reverse_lazy('eshopapp:adminproductsizelist')


class AdminProductSizeListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminproductsizelist.html'  
    model = Size
    context_object_name = 'adminproductsizelist' 
    

 
     
class AdminProductSizeUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/adminproductsizecreate.html'  
    model = Size
    form_class = AdminProductSizeCreateForm
    success_url = reverse_lazy('eshopapp:adminproductsizelist')


class AdminProductSizeDeleteView( AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminproductsizecreate.html'
    model = Size
    success_url = reverse_lazy('eshopapp:adminproductsizelist')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product Size deleted Successfully')
        return super(AdminProductSizeDeleteView,
                     self).delete(request, *args, **kwargs)    


class AjaxProductStatusChangeView(View):
    def get(self, request, **kwargs):
        product_id = self.request.GET.get('id')
        print(product_id)
        product = Product.objects.get(id=product_id)
        
        if product.is_active:
            product.is_active = False
            message = 'Product deactivated'
        else:
            product.is_active = True
            message = 'Product activated'
        product.save()    

        return JsonResponse({'message':message})  
     
         
class AjaxOrderStatusChangeView(View):
    def get(self, request, **kwargs):
        order_id = self.request.GET.get('id')
        value = self.request.GET.get('value')
        print(value)
        print(order_id)
        order = Order.objects.get(id=order_id)
        print(order)
        order.order_status = value
        order.save()
        # if product.is_active:
        #     product.is_active = False
        #     message = 'Product deactivated'
        # else:
        #     product.is_active = True
        #     message = 'Product activated'
        # product.save()    
        
        return JsonResponse({'message':'Order status changed'})        
    

#Sliders

class SliderCreateView(AdminRequiredMixin, CreateView):
    model = Slider
    template_name = 'admintemplates/slideradd.html'
    form_class = SliderForm
    success_url = reverse_lazy('eshopapp:adminsliderlist')



class SliderListView(AdminRequiredMixin,  ListView):
    model = Slider
    context_object_name = 'sliders'
    template_name = 'admintemplates/sliderlist.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['slider'] = Slider.objects.first()

        return context


class SliderDetailView( AdminRequiredMixin, DetailView):
    model = Slider
    template_name = 'admintemplates/sliderdetail.html'
    success_url = reverse_lazy('eshopapp:sliderdetail')

    context_object_name = 'sliderdetail'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        return context


class AdminSliderUpdateView(AdminRequiredMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'admintemplates/slideradd.html'
    # success_url = reverse_lazy("fweanapp:adminorganizationdetail")

    def get_success_url(self):

        return reverse_lazy('eshopapp:adminsliderlist')



# class AdminSliderDeleteView( DeleteView):
#     model = Slider
#     success_url = reverse_lazy('eshopapp:adminsliderlist')

#     def get(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)



#Client Views
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    



class ClientRequiredMixin(object):

    def get_context_data(self, **kwargs):
        # del self.request.session['cart_id']

        cart_id = self.request.session.get("cart_id", None)
        
        list1 = []
        
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            
            for a in cart.cartproduct_set.all():
                list1.append(a.subtotal)
        else:
            cart = None
        
        

        context = super().get_context_data(**kwargs)
        context['org'] = Organization.objects.first()
        context['slider'] = Slider.objects.first()
        context['allproductlist'] = Product.objects.filter(is_active=True)
        context['allcategories'] = ProductCategory.objects.filter(is_active=True)
        context['men_products'] = Product.objects.filter(is_active = True, main_category = 'Men\'s Wear')
        context['women_products'] = Product.objects.filter(is_active = True, main_category = 'Women\'s Wear')
        context['kid_products'] = Product.objects.filter(is_active = True, main_category = 'Kid\'s Wear')
        context['related_products'] = Product.objects.filter(is_active = True)
        context['cart'] = cart
        context['total'] = sum(list1)
        
        return context
    

class CustomerRegistrationView(ClientRequiredMixin,CreateView):
    template_name = "clienttemplates/customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("eshopapp:clienthome")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(ClientRequiredMixin,View):
    # template_name = "clienttemplates/clientbase.html"
    def get(self, request):
        logout(request)
        return redirect("eshopapp:customerlogin")


class CustomerLoginView(ClientRequiredMixin,FormView):
    template_name = "clienttemplates/customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("eshopapp:customerprofile")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class PasswordForgotView(ClientRequiredMixin,FormView):
    template_name = "clienttemplates/forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Eshop App',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(ClientRequiredMixin,FormView):
    template_name = "clienttemplates/passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/customer-login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)


class ClientHomeView(ClientRequiredMixin,TemplateView):
    template_name = 'clienttemplates/clienthome.html'


class ClientProductListView(ClientRequiredMixin,ListView):
    model = Product
    template_name = 'clienttemplates/clientproductlist.html'
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'allproductslist'

    paginate_by = 4

class ClientProductByMainCategoryListView(ClientRequiredMixin,ListView):
    model = Product
    template_name = 'clienttemplates/clientproductlistbymaincategory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        a = self.kwargs['str']


       
        if a == 'MensWear':
            wear = Product.objects.filter(main_category =  'Men\'s Wear' ,is_active = True)
            context['menswear'] = wear
        elif a == 'WomensWear':
            wear = Product.objects.filter(main_category =  'Women\'s Wear' ,is_active = True)
            context['womenswear'] = wear
        elif a == 'KidsWear':
            wear = Product.objects.filter(main_category =  'Kid\'s Wear' ,is_active = True)
            context['kidswear'] = wear
        elif a == 'Others':
            wear = Product.objects.filter(main_category =  'Others' ,is_active = True)
            context['others'] = wear

        return context
    # context_object_name = 'productlistbymaincategory'



class ClientProductByCategoryListView(ClientRequiredMixin,ListView):
    model = Product
    template_name = 'clienttemplates/clientproductlistbycategory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        a = self.kwargs['str']
        category = ProductCategory.objects.get(slug = a)

        print(category.id)
        
        products = Product.objects.filter(category__id = category.id)
        context['category_products'] = products

        return context
    # context_object_name = 'productlistbymaincategory'


class ClientProductDetailView(ClientRequiredMixin,DetailView):
    model = Product
    template_name = 'clienttemplates/clientproductdetail.html'
    context_object_name = 'productdetail'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        current_product_slug = self.kwargs['slug']
        
        
        # print('*-/-*-*-*-*-*')
        product = Product.objects.get(slug=current_product_slug)
        
        try:
            product_size_stock = ProductSizeStock.objects.filter(product=product)
        except:
            product_size_stock = None
        # print("////////")
        # print(product_size_stock)
        try:
            cart_id = self.request.session.get("cart_id", None)
            cart = Cart.objects.get(id=cart_id)
            # print(cart)
            pro_quantity = cart.cartproduct_set.get(product__slug=current_product_slug).quantity
            print(pro_quantity)
        except:
            pro_quantity  = 0

        try:
            pro_quantity_size = cart.cartproduct_set.get(product__slug=current_product_slug).quantity
            # print(str(pro_quantity_size) + '   ualala')
        except:
            pass    
        list = []
        for a in product.category.all():
            # print (a)
            list.append(a)
        # print(list)    
        related_products = Product.objects.exclude(slug=current_product_slug).filter(category__in = list)
        
        p_size_stock = ProductSizeStock.objects.filter(product=product)
        # for a in p_size_stock:
        #     print(a.size)
        context['related_products'] = related_products
        context['pro_quantity'] = pro_quantity
        context['pro_size_stock'] = p_size_stock
        return context


class ClientProductSizeQuantityView(ClientRequiredMixin, TemplateView):
    template_name = "clienttemplates/clientproductdetail.html"
    def get(self, request, *args, **kwargs):
        print("heyyyyyyyyyyy")
        print(self.request.GET)
        # token = request.POST.get('csrfmiddlewaretoken')
        

        # print (id)

        product = self.request.GET['product-kwargs']
        print (product)
        p_size = self.kwargs['pro_sizeqty']
        print(p_size)
        try:
            t_size = ProductSizeStock.objects.get(product__title=product, size__title=p_size)
            
            print(t_size.instock)
            data = {
            't_size' : t_size.product.title,
            't_size_stock' : t_size.instock,
        }
        except:

            data = {
            
        }
            
        
        return JsonResponse(data)    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.request.GET['product-kwargs']
        print (product)
        p_size = self.kwargs['pro_sizeqty']
        print(p_size)
        try:
            t_size = ProductSizeStock.objects.get(product__title=product, size__title=p_size)
            
            print(t_size.instock)
        except:
            pass    
            context['t_size'] = t_size.instock
            
            return context





class ClientProductSearchListView(ClientRequiredMixin, ListView):

    model = Product
    template_name = 'clienttemplates/clientproductsearchlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = self.request.GET.get('q')
        c =  self.request.GET.get('c')
      
        if c:
            category = ProductCategory.objects.get(title = c)
            search_products = Product.objects.filter(category = category.id).filter(
                Q(category__title__icontains = a)|
                Q(title__icontains = a )
                ).distinct()
            context['search_products'] = search_products
        else:
          
            search_products = Product.objects.filter(
                Q(category__title__icontains = a)|
                Q(title__icontains = a ), is_active = True
                ).distinct()
            context['search_products'] = search_products
        

        # else:
        #     context['search_products'] = Product.objects.filter(is_active=True)


        return context

    
class CustomerProfileView(ClientRequiredMixin,TemplateView):
    template_name = "clienttemplates/customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/customer-login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


#Cart







    
class AjaxProductQtyView(ClientRequiredMixin, TemplateView):
    template_name = "clienttemplates/addtocart.html"

    def get(self, request, *args, **kwargs):
        # print('hello') 
        cart_id = self.request.session.get("cart_id", None)

        product_id = self.kwargs['pro_id']
        product_obj = Product.objects.get(id=product_id)
        i_size = request.GET['item_size']
            
    
        if cart_id:

            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                        product=product_obj)    
            

           

            
            # x = CartProduct.objects.filter(quantity=product_obj)
            print('/////////////////////////////////////////////////////////')
            print(i_size)

            
           
           
            p_size = 'S'
            try:
                a = this_product_in_cart.get(product__title=product_obj.title, size__shortname=i_size)
                qty = a.quantity    
            except:
                qty = 0
            print('=====>' + str(qty))
            print(request.GET['item_size'])
            t_size = ProductSizeStock.objects.get(product__title=product_obj.title, size__shortname=i_size)
            d = t_size.instock
            
                
        else:
            qty = 0
            d = 0
            t_size = ProductSizeStock.objects.get(product__title=product_obj.title, size__shortname=i_size)
        
        # print(qty)

        

        return JsonResponse({
            'message': ' has been added to your cart',
            # 'addedproduct': product_obj.title,
            # 'addedproductcolor': product_obj.color.title,
            # 'addedproductsize': product_obj.size.title,
            'addedproductquantity': qty,
            't_size_stock': t_size.instock ,
            # 'addedproductprice': cartproduct.rate,
            # 'addedproductimage': product_obj.image1.url
        })    
    



class AjaxProductSizeView(ClientRequiredMixin, TemplateView):
    template_name = "clienttemplates/addtocart.html"

    def get(self, request, *args, **kwargs):
        print('hello') 
        cart_id = self.request.session.get("cart_id", None)
    
        if cart_id:
            
            

           

            product_id = self.kwargs['pro_id']
            product_obj = Product.objects.get(id=product_id)
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                    product=product_obj)
            
            # x = CartProduct.objects.filter(quantity=product_obj)
            print('size*******size*****size*******')
            # print()

            a = this_product_in_cart.last()
            if a:
                size = a.product.size.all()
                for s in size:
                    print(s)   
            
            else:
                # qty = 0
                pass
        else:
            # qty = 0
            pass
       
        
        # print(qty)

        

        return JsonResponse({
            'message': ' has been added to your cart',
            # 'addedproduct': product_obj.title,
            # 'addedproductcolor': product_obj.color.title,
            # 'addedproductsize': product_obj.size.title,
            # 'addedproductquantity': size,
            # 'addedproductprice': cartproduct.rate,
            # 'addedproductimage': product_obj.image1.url
        })    


class AjaxAddToCartView(ClientRequiredMixin, TemplateView):
    template_name = "clienttemplates/addtocart.html"

    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        size = request.GET.get('size')
        print(request.GET.get)
        print(size)
        item_quantity = int(request.GET.get('item_quantity'))
        product_obj = Product.objects.get(id=product_id)
        print('111111111111111111111111111')
        t_size = ProductSizeStock.objects.get(product__id=product_id,size__shortname = size)
        print(t_size.instock)
        q = CartProduct.objects.get(product__id=product_id)
        print(q)
        try:
            q = CartProduct.objects.get(product__id=product_id,size__shortname = size)
            print(q.quantity)
            t_q = q
        except:
            t_q = 0

        

        print(product_obj, product_id, item_quantity)
        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        sz = Size.objects.get(shortname = size)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id) 
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj, size__shortname = size)
            print(this_product_in_cart)
          
            
            # item already exists in cart
            if this_product_in_cart.exists(): 
                print('909090909090')
                cartproduct = this_product_in_cart.filter(cart= cart_obj)
                # for cartproducts in cartproduct:
                print(cartproduct)
                # p_s_s = ProductSizeStock.objects.filter(product = cartproduct.product, size__shortname = size)
                # print(p_s_s)
                # print(this_product_in_cart) 6
                for cartproduct in cartproduct:
                    sz = Size.objects.get(shortname = size)
                    print(sz)
                    print(cartproduct.product)
                    print('????????????'+ str(sz.shortname))
                    print(cartproduct.size.all())
                    if sz in cartproduct.size.all() :
                        print('yes')
                        cartproduct.quantity += item_quantity
                        if product_obj.selling_price and (product_obj.selling_price != 0) :
                            cartproduct.subtotal = product_obj.selling_price * cartproduct.quantity
                            cartproduct.rate = product_obj.selling_price
                            cartproduct.save()
                            cart_obj.total += (product_obj.selling_price * item_quantity)
                            cart_obj.save()
                            
                        else:
                            cartproduct.subtotal = product_obj.marked_price * cartproduct.quantity
                            cartproduct.rate = product_obj.marked_price   
                            cartproduct.save()
                            cart_obj.total += (product_obj.marked_price * item_quantity)
                            cart_obj.save()

                    else:
                        if product_obj.selling_price and product_obj.selling_price != 0:
                            cartproduct = CartProduct.objects.create(
                                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=item_quantity, subtotal=(product_obj.selling_price * item_quantity))
                            cartproduct.size.add(sz)
                            cart_obj.total += (product_obj.selling_price * item_quantity)
                            cart_obj.save()
                        else:
                            cartproduct = CartProduct.objects.create(
                                cart=cart_obj, product=product_obj, rate=product_obj.marked_price, quantity=item_quantity, subtotal=(product_obj.marked_price * item_quantity))
                            cartproduct.size.add(sz)
                            cart_obj.total += (product_obj.marked_price * item_quantity)
                            cart_obj.save()


            # new item is added in cart
            else:
                if product_obj.selling_price and product_obj.selling_price != 0:
                    cartproduct = CartProduct.objects.create(
                        cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=item_quantity, subtotal=(product_obj.selling_price * item_quantity))
                    cartproduct.size.add(sz)
                    cart_obj.total += (product_obj.selling_price * item_quantity)
                    cart_obj.save()
                else:
                    cartproduct = CartProduct.objects.create(
                        cart=cart_obj, product=product_obj, rate=product_obj.marked_price, quantity=item_quantity, subtotal=(product_obj.marked_price * item_quantity))
                    cartproduct.size.add(sz)
                    cart_obj.total += (product_obj.marked_price * item_quantity)
                    cart_obj.save()

        else:
           
            print('????????????'+ str(sz.shortname))
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            if product_obj.selling_price and product_obj.selling_price != 0:
                sz = Size.objects.get(shortname = size)
                print('nmnbnm'+ str(sz))
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=item_quantity, subtotal=product_obj.selling_price)
                
                cartproduct.size.add(sz)
            
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:   

                sz = Size.objects.get(shortname = size)
                print('nmnbnm'+ str(sz)) 
               
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.marked_price, quantity=item_quantity, subtotal=product_obj.marked_price)
                cartproduct.size.add(sz)
            
                cart_obj.total += product_obj.marked_price
                cart_obj.save()
        

        return JsonResponse({
            'message': ' has been added to your cart',
            'addedproduct': product_obj.title,
            # 'addedproductcolor': product_obj.color.title,
            # 'addedproductsize': product_obj.size.title,
            'addedproductquantity': item_quantity,
            't_size': t_size.instock,
            't_q': t_q,
            
            'addedproductprice': cartproduct.rate,
            'addedproductimage': product_obj.image1.url
        })    




class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            
          
            
            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
              
                cartproduct.quantity += 1
                if product_obj.selling_price and (product_obj.selling_price != 0):
                    cartproduct.subtotal = product_obj.selling_price * cartproduct.quantity
                    cartproduct.rate = product_obj.selling_price
                    cartproduct.save()
                    cart_obj.total += product_obj.selling_price * cartproduct.quantity
                    cart_obj.save()
                    
                else:
                    cartproduct.subtotal = product_obj.marked_price * cartproduct.quantity
                    cartproduct.rate = product_obj.marked_price   
                    cartproduct.save()
                    cart_obj.total += product_obj.marked_price * cartproduct.quantity
                    cart_obj.save()
            # new item is added in cart
            else:
                if product_obj.selling_price and product_obj.selling_price != 0:
                    cartproduct = CartProduct.objects.create(
                        cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                    cart_obj.total += product_obj.selling_price
                    cart_obj.save()
                else:
                    cartproduct = CartProduct.objects.create(
                        cart=cart_obj, product=product_obj, rate=product_obj.marked_price, quantity=1, subtotal=product_obj.marked_price)
                    cart_obj.total += product_obj.marked_price
                    cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            if product_obj.selling_price and product_obj.selling_price != 0:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            else:    
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.marked_price, quantity=1, subtotal=product_obj.marked_price)
                cart_obj.total += product_obj.marked_price
                cart_obj.save()

        return JsonResponse({
            'message': ' has been added to your cart',
            # 'addedproduct': product_obj.title,
            # 'addedproductcolor': productsku.color.title,
            # 'addedproductsize': productsku.size.title,
            # 'addedproductquantity': item_quantity,
            # 'addedproductprice': productsku.selling_price,
            # 'addedproductimage': productsku.productimage_set.first().image.url
        })        







class MyCartView( ClientRequiredMixin, TemplateView):
    template_name = "clienttemplates/mycart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        list1 = []
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            
            for a in cart.cartproduct_set.all():
                
                list1.append(a.subtotal)


         
            # print(sum(list1))
        else:
            cart = None

            
        context['cart'] = cart
        context['total'] = sum(list1)
        return context


class EmptyCartView( View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
            del self.request.session['cart_id']
        return redirect("eshopapp:mycart")


class ManageCartView(View):
    def get(self, request, *args, **kwargs):

        # print('-*--*-/*-/-/-*/*-/*-/*')
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("eshopapp:mycart")


class CheckoutView(ClientRequiredMixin, CreateView):
    template_name = "clienttemplates/checkout.html"
    form_class = CheckoutForm
    model = Order
    success_url = reverse_lazy("eshopapp:clienthome")

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated and request.user.customer:
    #         pass
    #     else:
    #         return redirect("/customer-login/?next=/checkout/")
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        print(cart_id)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            print(cart_obj)
            print('????')
            # print(form.instance)
            for a in cart_obj.cartproduct_set.all():
                print(a)
                
            #     print(a.quantity)
            #     e = a.quantity
            #     d = a.product.instock
            #     print(d)
            #     a.product.instock = d-e
            #     a.product.save()
            #     a.save()
   
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            # pm = form.cleaned_data.get("payment_method")
            order = form.save()
            # if pm == "Khalti":
            #     return redirect(reverse("ecomapp:khaltirequest") + "?o_id=" + str(order.id))
            # elif pm == "Esewa":
            #     return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("eshopapp:clienthome")
        return super().form_valid(form)


class CustomerOrderDetailView(ClientRequiredMixin,DetailView):
    template_name = "clienttemplates/customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("eshopapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)
    