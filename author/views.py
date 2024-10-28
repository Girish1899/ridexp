import os
from django.shortcuts import get_object_or_404, render
from superadmin.models import Blogs, PackageCategories, PackageCategoriesHistory, Packages, RideDetails,Customer,Driver,Vehicle, WebsitePackages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.text import slugify
from superadmin.models import Profile,User
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

@login_required(login_url='login')
def index(request):
    cust_count = Customer.objects.count()
    driver_count = Driver.objects.count()
    booking_count = RideDetails.objects.count()
    vehicle_count = Vehicle.objects.count()

    context = {
        'cust_count': cust_count,
        'driver_count': driver_count,
        'booking_count': booking_count,
        'vehicle_count': vehicle_count,
    }
    return render(request,'author/index.html',context)

@login_required
def author_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user, type='author')
    return render(request, 'author/app-profile.html', {'profile': profile})


@login_required(login_url='login')   
def check_package_category(request):
    category_name = request.GET.get('category_name', None)
    cp = PackageCategories.objects.filter(category_name=category_name)
    data = {
        'exists': cp.count() > 0
    }
    return JsonResponse(data) 

@method_decorator(login_required(login_url='login'), name='dispatch')
class addpackagecategory(TemplateView):
    template_name = "author/add_package_category.html"

    def post(self, request):
        category_name = request.POST['category_name']

        cl = PackageCategories(
            category_name=category_name,
            created_by=request.user,
            updated_by=request.user
        )
        cl.save()
        return JsonResponse({'status': "Success"})

@method_decorator(login_required(login_url='login'), name='dispatch')
class PackageCategoryList(ListView):
    model = PackageCategories
    template_name = "author/view_package_category.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletePackageCategory(View):
    def get(self, request):
        package_category_id = request.GET.get('package_category_id', None)
        PackageCategories.objects.get(package_category_id=package_category_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPackageCategory(TemplateView):
    template_name = 'author/edit_package_category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['package_category_id'] = self.kwargs['id']
            plist = PackageCategories.objects.filter(package_category_id=context['package_category_id'])
        except:
            plist = PackageCategories.objects.filter(package_category_id=context['package_category_id'])
            
        context['plist']= list(plist)
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdatePackageCategory(APIView):
    def post(self, request):
        package_category_id = request.POST['package_category_id']
        package = PackageCategories.objects.get(package_category_id=package_category_id)

        package.category_name = request.POST['category_name']
        package.updated_by = request.user
        package.save()

        PackageCategoriesHistory.objects.create(
            package_category_id=package.package_category_id,
            category_name=package.category_name,
            created_on=package.created_on,
            updated_on=package.updated_on,
            created_by=package.created_by.username if package.created_by else None,
            updated_by=request.user.username
        )

        return JsonResponse({'success': True}, status=200)

class PackageCategoryHistoryView(TemplateView):
    template_name = 'author/history_package_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_category_id = self.kwargs['package_category_id']
        package = get_object_or_404(PackageCategories, package_category_id=package_category_id)
        history = PackageCategoriesHistory.objects.filter(package_category_id=package_category_id).order_by('updated_on')
        context['package'] = package
        context['history'] = history
        return context
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class addwebpackages(TemplateView):
    template_name = "author/add_webpackages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pclist = PackageCategories.objects.all()
        context = {'pclist': list(pclist)}
        return context

    def post(self, request):
        try:
            print("POST request received")

            title = request.POST.get('title')
            slug = slugify(title)
            package_category_id = request.POST.get('package_category')
            description = request.POST.get('description')
            top_attraction = request.POST.get('top_attraction')
            why_visit = request.POST.get('why_visit')
            package_highlights = request.POST.get('package_highlights')
            image = request.FILES.get('image')
            image_link = request.POST.get('image_link')
            facebook_link = request.POST.get('facebook_link')
            instagram_link = request.POST.get('instagram_link')
            whatsapp_link = request.POST.get('whatsapp_link')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            tags = request.POST.get('tags')
            h1tag = request.POST.get('h1tag')
            status = request.POST.get('status')

            print(f"Form data: title={title}, category_id={package_category_id}, description={description}")

            if not title or not package_category_id:
                print("Missing required fields: title or category")
                return JsonResponse({'status': "Failed", 'error': "Title and category are required."}, status=400)

            try:
                package_category = PackageCategories.objects.get(package_category_id=package_category_id)
            except PackageCategories.DoesNotExist:
                print(f"Package category not found: {package_category_id}")
                return JsonResponse({'status': "Failed", 'error': "Invalid package category."}, status=400)

            webpackage = WebsitePackages(
                title=title,
                slug=slug,
                package_category=package_category,
                description=description,
                top_attraction=top_attraction,
                why_visit=why_visit,
                package_highlights=package_highlights,
                image=image,
                image_link=image_link,
                facebook_link=facebook_link,
                instagram_link=instagram_link,
                whatsapp_link=whatsapp_link,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                tags=tags,
                h1tag=h1tag,
                status=status,
                created_by=request.user,
                updated_by=request.user
            )

            webpackage.save()
            print("Package saved successfully")
            return JsonResponse({'status': "Success"})

        except Exception as e:
            print(f"Error saving package: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class webPackageList(ListView):
    model = WebsitePackages
    template_name = "author/view_webpackages.html"
    context_object_name = 'webpackages'
    
    def get_queryset(self):
        return WebsitePackages.objects.filter(created_by=self.request.user)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletewebPackages(View):
    def get(self, request):
        webpackage_id = request.GET.get('webpackage_id', None)
        WebsitePackages.objects.get(webpackage_id=webpackage_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditwebPackages(TemplateView):
    template_name = 'author/edit_webpackages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pclist = PackageCategories.objects.all()
        try:
            context['webpackage_id'] = self.kwargs['id']
            package = WebsitePackages.objects.filter(webpackage_id=context['webpackage_id'])
        except:
            package = WebsitePackages.objects.filter(webpackage_id=context['webpackage_id'])
        context = {'pclist': list(pclist), 'package': list(package)}
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdatewebPackages(APIView):
    def post(self, request):
        webpackage_id = request.POST['webpackage_id']
        title = request.POST['title']
        print("########",title)
        slug = slugify(title)
        package_category = request.POST['package_category']
        description = request.POST['description']
        top_attraction = request.POST['top_attraction']
        why_visit = request.POST['why_visit']
        package_highlights = request.POST['package_highlights']
        image = request.FILES.get('image')

        image_link = request.POST['image_link']
        facebook_link = request.POST['facebook_link']
        instagram_link = request.POST['instagram_link']
        whatsapp_link = request.POST['whatsapp_link']
        tags = request.POST['tags']
        meta_title = request.POST['meta_title']
        meta_description = request.POST['meta_description']
        meta_keywords = request.POST['meta_keywords']
        h1tag = request.POST['h1tag']
        status = request.POST['status']

        package_categoryIdobj = PackageCategories.objects.get(package_category_id=package_category)

        webpack = WebsitePackages.objects.get(webpackage_id=webpackage_id)


        webpack.title= title
        print("######## 2 ",title)
        webpack.slug=slug
        webpack.package_category= package_categoryIdobj
        webpack.description= description
        webpack.top_attraction= top_attraction
        webpack.why_visit= why_visit
        webpack.package_highlights= package_highlights
        webpack.image_link= image_link
        if image:
            webpack.image = image
        webpack.facebook_link= facebook_link
        webpack.instagram_link= instagram_link
        webpack.whatsapp_link= whatsapp_link
        webpack.tags= tags
        webpack.meta_title= meta_title
        webpack.meta_description= meta_description
        webpack.meta_keywords= meta_keywords
        webpack.h1tag= h1tag
        webpack.status=status
        webpack.updated_by = request.user
        webpack.save()
        
        return JsonResponse({'success': True}, status=200) 


@login_required(login_url='login')
def check_blogtitle(request):
    title = request.GET.get('title', None)
    titles = Blogs.objects.filter(title=title)
    data = {
        'exists': titles.count() > 0
    }
    return JsonResponse(data)
   
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddBlogView(TemplateView):
    template_name = "author/add_blog.html"

    def post(self, request):
        try:
            print("POST request received")

            title = request.POST.get('title')
            slug = slugify(title)
            description = request.POST.get('description')
            image = request.FILES.get('image')
            image_link = request.POST.get('image_link')
            facebook = request.POST.get('facebook_link')
            instagram = request.POST.get('instagram_link')
            whatsapp = request.POST.get('whatsapp_link')
            tags = request.POST.get('tags')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            h1tag = request.POST.get('h1tag')
            backlink = request.POST.get('backlink')
            related_bloglink = request.POST.get('related_bloglink')

            blog = Blogs(
                title=title,
                slug=slug,
                description=description,
                image_link=image_link,
                facebook=facebook,
                instagram=instagram,
                whatsapp=whatsapp,
                tags=tags,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                h1tag=h1tag,
                backlink=backlink,
                related_bloglink=related_bloglink,
                created_by=request.user,
                updated_by=request.user
            )

            if image:
                try:
                    print(f"Processing image: {image.name}")
                    img = Image.open(image)
                    img = img.resize((880, 450), Image.LANCZOS)
                    file_extension = os.path.splitext(image.name)[1].lower()

                    format = 'JPEG' if file_extension in ['.jpg', '.jpeg'] else 'PNG' if file_extension == '.png' else 'GIF'

                    img_io = BytesIO()
                    img.save(img_io, format=format)
                    img_content = ContentFile(img_io.getvalue(), image.name)
                    blog.image.save(image.name, img_content, save=False)
                except Exception as img_error:
                    print(f"Error processing image: {img_error}")
                    return JsonResponse({'status': "Failed", 'error': "Error processing image."}, status=400)

            blog.save()
            print("Blogs saved successfully")
            return JsonResponse({'status': "Success"})

        except Exception as e:
            print(f"Error saving blogs: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)

@method_decorator(login_required(login_url='login'), name='dispatch')
class BlogListView(ListView):
    model = Blogs
    template_name = "author/view_blog.html"
    context_object_name = 'blogs'
    
    def get_queryset(self):
        return Blogs.objects.filter(created_by=self.request.user)

@method_decorator(login_required(login_url='login'), name='dispatch')
class webDeleteBlogs(View):
    def get(self, request):
        blogs_id = request.GET.get('blogs_id', None)
        Blogs.objects.get(blogs_id=blogs_id).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@method_decorator(login_required(login_url='login'), name='dispatch')
class EditwebBlogs(TemplateView):
    template_name = 'author/edit_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['blogs_id'] = self.kwargs['id']
            blog = Blogs.objects.filter(blogs_id=context['blogs_id'])
        except:
            blog = Blogs.objects.filter(blogs_id=context['blogs_id'])
        context = {'blog': list(blog)}
        return context 
    
class UpdatewebBlogs(APIView):
    def post(self, request):
        blogs_id = request.POST.get('blogs_id')
        title = request.POST.get('title')
        slug = slugify(title)
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image_link = request.POST.get('image_link')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        whatsapp = request.POST.get('whatsapp')
        backlink = request.POST.get('backlink')
        related_bloglink = request.POST.get('related_bloglink')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        h1tag = request.POST.get('h1tag')

        try:
            blog = Blogs.objects.get(blogs_id=blogs_id)
        except Blogs.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'}, status=404)

        blog.title = title
        blog.slug=slug
        blog.description = description
        if image:
            blog.image = image  
        blog.image_link = image_link
        blog.facebook = facebook
        blog.instagram = instagram
        blog.whatsapp = whatsapp
        blog.backlink = backlink
        blog.related_bloglink = related_bloglink
        blog.meta_title = meta_title
        blog.meta_description = meta_description
        blog.meta_keywords = meta_keywords
        blog.h1tag = h1tag

        blog.save()

        return JsonResponse({'success': True}, status=200)    
