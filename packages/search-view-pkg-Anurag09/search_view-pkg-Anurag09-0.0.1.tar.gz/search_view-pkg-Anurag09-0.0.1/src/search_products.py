class SearchProducts:
    def search_view(request):
        # whatever user write in search box we get in query
        query = request.GET['query']
        products=models.Product.objects.all().filter(name__icontains=query)
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            counter=product_ids.split('|')
            product_count_in_cart=len(set(counter))
        else:
            product_count_in_cart=0

        # word variable will be shown in html when user click on search button
        word="Searched Result :"

        if request.user.is_authenticated:
            return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
        return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
