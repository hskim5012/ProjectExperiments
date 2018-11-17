from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Job
import bcrypt

# Create your views here.
def index(request):
    #Check is still logged in
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, 'Users/index.html')

def registrationprocess(request):
    #Run validations
    errors = User.objects.validator(request.POST)
    #run the validation messsages
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        #if successfully pass validations, bcrypt password
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        #insert into database for the registered user
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pwhash)
        #create a session that shows the user first name when logged in
        request.session['name'] = request.POST['first_name']
        #save the user ID for future needs (which is always)
        request.session['user_id'] = user.id
        #display successfu
        messages.add_message(request, messages.INFO, "Successfully logged-in!")
        return redirect('/dashboard')

def login(request):
    #check if logged in
    if 'user_id' in request.session:
        return redirect('/')
    #run validations to check for login (email and password)
    errors = User.objects.loginvalidator(request.POST)
    #pop messages if failure occurs
    if len(errors):
        for key,values in errors.items():
            messages.error(request, values)
        return redirect('/')
    else:
        #need to get user name via querying by email
        request.session['name'] = User.objects.get(email=request.POST['email']).first_name
        #also get user_id which important for everything
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/dashboard')

def dashboard(request):
    #check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    #create context to pass information to render
    context = {}
    #create a query with user to get name to render through context via show name without using sessions
    user = User.objects.get(id=request.session['user_id'])
    context['username'] = f'{user.first_name} {user.last_name}'
    jobs = Job.objects.all()
    context['jobs'] = jobs
    context['user'] = user
    return render(request,'Users/dashboard.html', context)

def logout(request):
    #delete current session
    request.session.clear()
    #display messages if logged out
    messages.add_message(request, messages.INFO, "You have been logged out.")
    return redirect('/')

def createJobs(request):
    ##check if logged in
    if not 'user_id' in request.session:
        return redirect('/')
    ##renders the page
    return render(request, "Users/new_jobs.html")

def jobprocessing(request):
    #check if logged in
    if not 'user_id' in request.session:
        return redirect('/')
    ##start validation
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/jobs/new')
    else:
        #needed to create an empty string to store the value since not able to pass it via request.POST
        category = ""
        #check the name in html and if matches add into the empty string
        if "pet_care" in request.POST:
            category = category + " Pet care, "
        if "garden" in request.POST:
            category = category + " Garden, "
        if "electrical" in request.POST:
            category = category + " Electrical, "
        if "other" in request.POST:
            category = category + request.POST['other']
        # if validation pass, start creating entry into the database, this has 2 one to many relationships (ie job_poster and job_taker)
        owner = User.objects.get(id=request.session['user_id'])
        ##defaulted all jobs to 1 person for the ability to take on jobs
        hire = User.objects.get(id=1)
        #create entry
        Job.objects.create(title=request.POST['title'], description=request.POST['description'], location=request.POST['location'], job_poster = owner, job_taker = hire, category=category)
        return redirect ('/dashboard')

def editpage(request, id):
    ##check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')

    ## return context to display the information into labels with values assigned in the html portion in the html to prepopulate
    context = {
        "job": Job.objects.get(id=id)
    }
    #renders the information
    return render(request, "Users/edit_page.html", context)

def jobeditprocessing(request, id):
    #check if logged in
    if not 'user_id' in request.session:
        return redirect('/')
    ##start validations
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/jobs/edit/'+id)
    else:
        ##start to update an existing job in the database by grabbing its "id"
        job = Job.objects.get(id=id)
        ##changes the title to what was submitted
        job.title = request.POST['title']
        ##changes the description
        job.description = request.POST['description']
        ##hanges the location
        job.location = request.POST['location']
        ##saves the job
        job.save()
        ##displays a success message
        messages.success(request, 'Job was successfully updated!')
        return redirect('/dashboard')

def jobprofile(request, id):
    ##check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    #display the information of the job through job and get user name through the user objects to display name
    context = {
        "job": Job.objects.get(id=id),
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "Users/job_profile.html", context)

def deletejob(request, id):
    #check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    #no validations and straight to deletion of the job via filtering of the id
    unwanted = Job.objects.filter(id=id)
    #deletes from database
    unwanted.delete()
    return redirect ('/dashboard')

def addjob(request, id):
    #check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    job = Job.objects.get(id=id)
    # print("getting logged in user id")
    print(job.job_taker)
    job.job_taker = User.objects.get(id=request.session['user_id'])
    job.save()
    # print(job.job_taker.first_name)
    return redirect('/dashboard')

# def jobcompleted(request, id):
#     #check if not logged in
#     if not 'user_id' in request.session:
#         return redirect('/')
#     #grabs the job id by filtering in the database
#     job = Job.objects.filter(id=id)
#     #deletes the job from database
#     job.delete()
#     return redirect ('/dashboard')

def giveupjob(request, id):
    #check if not logged in
    if not 'user_id' in request.session:
        return redirect('/')
    #grab the job information
    job = Job.objects.get(id=id)
    #assigns the the job back to the the first id
    job.job_taker = User.objects.get(id=1)
    #Use just "job.save()" instead of job.job_taker.save() <-- this does not save
    job.save()
    return redirect ('/dashboard')
