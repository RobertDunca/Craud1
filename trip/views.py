from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.list import MultipleObjectMixin

from trip.filters import EventFilter, RestaurantFilter
from trip.forms import EventForm, ReviewForm
from trip.models import Event, Restaurant, Review


class FilteredListView(ListView):
    filter_class = None
    filtered_set = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filtered_set = self.filter_class(self.request.GET, queryset=queryset)
        return self.filtered_set.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered_set
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = 'reviews/create_review.html'
    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def form_valid(self, form):
        if form.is_valid():
            review = form.save(commit=False)
            review.user = self.request.user
            review.save()
            review_model = self.request.POST.get('review_model')
            id_ = self.request.POST.get('id')
            if review_model == 'event':
                event = Event.objects.get(pk=id_)
                event.reviews.add(review)
                event.save()
            return redirect(self.get_success_url())


class EventCreateView(LoginRequiredMixin, CreateView):
    template_name = 'events/create_event.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('create_new_event')


class EventListView(ListView):
    template_name = 'events/list_of_events.html'
    model = Event
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        data = super(EventListView, self).get_context_data()
        events = Event.objects.all()
        event_filter = EventFilter(self.request.GET, queryset=events)
        data['all_events'] = event_filter.qs
        data['event_filter'] = event_filter

        return data


class EventDetailView(DetailView):
    template_name = 'events/event_details.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = ReviewForm()
        return context


class RestaurantCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'restaurants/create_restaurant.html'
    model = Restaurant
    form_class = EventForm
    success_url = reverse_lazy('create_new_restaurant')


class RestaurantListView(FilteredListView, MultipleObjectMixin):
    template_name = 'restaurants/list_of_restaurants.html'
    paginate_by = 5
    model = Restaurant
    filter_class = RestaurantFilter
    context_object_name = 'all_restaurants'

    # def get_context_data(self, **kwargs):
    #     data = super(RestaurantListView, self).get_context_data()
    #     restaurants = Restaurant.objects.all()
    #     restaurant_filter = RestaurantFilter(self.request.GET, queryset=restaurants)
    #     restaurants = list(restaurants)
    #     restaurants = list(filter(lambda restaurant: restaurant.average_rating() > 3, restaurants))
    #     restaurants.sort(key=lambda restaurant: restaurant.average_rating(), reverse=True)
    #     data['all_restaurants'] = restaurant_filter.qs
    #     data['restaurant_filter'] = restaurant_filter
    #
    #     return data
    #
    # def get_queryset(self):
    #     filtered_qs = filters.RestaurantFilter(self.request.GET, queryset=Restaurant.objects.all()).qs
    #     paginator = Paginator(filtered_qs, 5)
    #     page = self.request.GET.get('page')
    #     try:
    #         response = paginator.page(page)
    #     except PageNotAnInteger:
    #         response = paginator.page(1)
    #     except EmptyPage:
    #         response = paginator.page(paginator.num_pages)
    #
    #     return response


class ThingToDoCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'things_to_do/create_ttd.html'
    model = Restaurant
    form_class = EventForm
    success_url = reverse_lazy('create_new_ttd')


class ThingToDoListView(ListView):
    template_name = 'things_to_do/list_of_ttd.html'
    model = Restaurant
    context_object_name = 'all_ttd'
