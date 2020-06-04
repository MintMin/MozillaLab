from django.shortcuts import render
from .models import Career_Fair, Career_Booth
from accounts.models import Student, Recruiter
from django.views.generic import TemplateView

class CareerFairDashboard(TemplateView):
	template_name = 'career_fair/career_fair_dashboard.html'
	def get_context_data(self, **kwargs):
		request = self.request
		context = super(CareerFairDashboard, self).get_context_data(**kwargs)
		student = Student.objects.filter(user = request.user)[0]
		if(request.user.is_student):
			context['career_list'] = Career_Fair.objects.filter(university = student.university).order_by('date')
		elif(request.user.is_recruiter):
			context['career_list'] = Career_Fair.objects.all().order_by('date')
		return context