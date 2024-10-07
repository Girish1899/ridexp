import os
from django.shortcuts import get_object_or_404, render
from superadmin.models import Blogs, PackageCategories, PackageCategoriesHistory, Packages, RideDetails,Customer,Driver,Vehicle, WebsitePackages
from django.contrib.auth.decorators import login_required
# views.py
from django.http import JsonResponse
from superadmin.models import Profile,User
from rest_framework.views import APIView
from django.views.generic import TemplateView,ListView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your views here.

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

# package category #######################################################################

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

        # Update the ride type with new data
        package.category_name = request.POST['category_name']
        package.updated_by = request.user
        package.save()

        # Create another RidetypeHistory entry after updating the ride type
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
    

# packages ############
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
            # Print that the POST request is received
            print("POST request received")

            # Retrieve data from POST request
            title = request.POST.get('title')
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
            author = request.POST.get('author')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            h1tag = request.POST.get('h1tag')

            # Print received form data
            print(f"Form data: title={title}, category_id={package_category_id}, description={description}")

            # Validate required fields
            if not title or not package_category_id:
                print("Missing required fields: title or category")
                return JsonResponse({'status': "Failed", 'error': "Title and category are required."}, status=400)

            # Fetch category object
            try:
                package_category = PackageCategories.objects.get(package_category_id=package_category_id)
            except PackageCategories.DoesNotExist:
                print(f"Package category not found: {package_category_id}")
                return JsonResponse({'status': "Failed", 'error': "Invalid package category."}, status=400)

            # Create package object
            webpackage = WebsitePackages(
                title=title,
                package_category=package_category,
                description=description,
                top_attraction=top_attraction,
                why_visit=why_visit,
                package_highlights=package_highlights,
                image_link=image_link,
                facebook_link=facebook_link,
                instagram_link=instagram_link,
                whatsapp_link=whatsapp_link,
                author=author,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                h1tag=h1tag,
                created_by=request.user,
                updated_by=request.user
            )

            # Process image if uploaded
            if image:
                try:
                    print(f"Processing image: {image.name}")
                    img = Image.open(image)
                    img = img.resize((880, 450), Image.LANCZOS)
                    file_extension = os.path.splitext(image.name)[1].lower()

                    # Define format based on extension
                    format = 'JPEG' if file_extension in ['.jpg', '.jpeg'] else 'PNG' if file_extension == '.png' else 'GIF'

                    img_io = BytesIO()
                    img.save(img_io, format=format)
                    img_content = ContentFile(img_io.getvalue(), image.name)
                    webpackage.image.save(image.name, img_content, save=False)
                except Exception as img_error:
                    print(f"Error processing image: {img_error}")
                    return JsonResponse({'status': "Failed", 'error': "Error processing image."}, status=400)

            # Save the package
            webpackage.save()
            print("Package saved successfully")
            return JsonResponse({'status': "Success"})

        except Exception as e:
            # Print the exception
            print(f"Error saving package: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class webPackageList(ListView):
    model = WebsitePackages
    template_name = "author/view_webpackages.html"

@method_decorator(login_required(login_url='login'), name='dispatch')
class DeletewebPackages(View):
    def get(self, request):
        package_id = request.GET.get('package_id', None)
        WebsitePackages.objects.get(package_id=package_id).delete()
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
            context['package_id'] = self.kwargs['id']
            plist = WebsitePackages.objects.filter(package_id=context['package_id'])
        except:
            plist = WebsitePackages.objects.filter(package_id=context['package_id'])
        context = {'pclist': list(pclist), 'plist': list(plist)}
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateCategory(APIView):
    def post(self, request):
        package_id = request.POST['package_id']
        webpack = get_object_or_404(WebsitePackages, package_id=package_id)
        original_status = webpack.status

        # Update the category with new data
        webpack.title = request.POST['title']
        webpack.description = request.POST['description']
        webpack.top_attraction = request.POST['top_attraction']
        if 'image' in request.FILES:
            # Handle image resizing before saving
            image = request.FILES['image']
            img = Image.open(image)
            
            # Resize image to 880x350 pixels
            img = img.resize((880, 450), Image.LANCZOS)

            # Get the file extension and set the appropriate format
            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg']:
                format = 'JPEG'
            elif file_extension == '.png':
                format = 'PNG'
            elif file_extension == '.gif':
                format = 'GIF'
            else:
                format = 'JPEG'  # Default format if none of the above match

            # Save the image to an in-memory file
            img_io = BytesIO()
            img.save(img_io, format=format)
            img_content = ContentFile(img_io.getvalue(), image.name)

            # Assign the resized image to the category object
            webpack.image.save(image.name, img_content, save=False)
            webpack.status = request.POST['status']
            webpack.updated_by = request.user
            webpack.save()

        return JsonResponse({'success': True}, status=200)
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class AddBlogView(TemplateView):
    template_name = "author/add_blog.html"

    def post(self, request):
        try:
            print("POST request received")

            # Retrieve data from POST request
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            image_link = request.POST.get('image_link')
            facebook = request.POST.get('facebook_link')
            instagram = request.POST.get('instagram_link')
            whatsapp = request.POST.get('whatsapp_link')
            author = request.POST.get('author')
            meta_title = request.POST.get('meta_title')
            meta_description = request.POST.get('meta_description')
            meta_keywords = request.POST.get('meta_keywords')
            h1tag = request.POST.get('h1tag')
            backlink = request.POST.get('backlink')
            related_bloglink = request.POST.get('related_bloglink')

            blog = Blogs(
                title=title,
                description=description,
                image_link=image_link,
                facebook=facebook,
                instagram=instagram,
                whatsapp=whatsapp,
                author=author,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                h1tag=h1tag,
                backlink=backlink,
                related_bloglink=related_bloglink,
                created_by=request.user,
                updated_by=request.user
            )

            # Process image if uploaded
            if image:
                try:
                    print(f"Processing image: {image.name}")
                    img = Image.open(image)
                    img = img.resize((880, 450), Image.LANCZOS)
                    file_extension = os.path.splitext(image.name)[1].lower()

                    # Define format based on extension
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
            # Print the exception
            print(f"Error saving blogs: {e}")
            return JsonResponse({'status': "Failed", 'error': str(e)}, status=500)

@method_decorator(login_required(login_url='login'), name='dispatch')
class BlogListView(ListView):
    model = Blogs
    template_name = "author/view_blog.html"

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
    template_name = 'author/edit_blogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['blogs_id'] = self.kwargs['id']
            blist = Blogs.objects.filter(blogs_id=context['blogs_id'])
        except:
            blist = Blogs.objects.filter(blogs_id=context['blogs_id'])
        context = {'blist': list(blist)}
        return context 
