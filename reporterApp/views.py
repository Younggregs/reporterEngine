# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage, send_mail
from django.core import serializers
from .models import Account, Category, Location, Impact, Report
from .serializers import AccountSerializer, NewAccountSerializer, ErrorCheckSerializer, SuccessCodeSerializer, LocationSerializer, CategorySerializer, ImpactSerializer, ReportSerializer, UserSerializer, ReportTypeAggregateSerializer, AggregateSerializer, MyReportAggregateSerializer









def authenticateLogin(request, username, password):

    success = False

    try: 
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            success = True
    except: 
        pass

    return success















def getAccount(request):

    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        email = user.username

        account = Account.objects.get(email=email)
        return account

    else:
        
        return -1










class Login(APIView):

    def get(self,request):
        
        account = Account.objects.all()
        serializer = UserSerializer(account, many=True)

        return Response(serializer.data)



    def post(self,request):

        serializer = NewAccountSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.data['name']
            email = serializer.data['email']
            password = serializer.data['password']

            try:

                User.objects.get(username = email)
                Account.objects.get(email = email)
                
                status = authenticateLogin(request, email, password)
                
                if status : 
                    code = email
                    success = {
                        'code' : code
                    }

                    serializer = SuccessCodeSerializer(success, many = False)
                    return Response(serializer.data)

                else:

                    error_message = 'Oops login details do not match'
                    err = {
                        'error_message' : error_message
                    }

                    serializer = ErrorCheckSerializer( err, many=False)
                    return Response(serializer.data)

            except:
                
                pass


            
            raw_password = password
            password = make_password(password)
            

            user = User()
            user.username = email
            user.password = password
            user.name = name
            user.save()

            account = Account()
            account.name = name
            account.email = email
            account.password = password
            account.save()

            code = email
            success = {
                'code' : code
            }

            serializer = SuccessCodeSerializer(success , many = False)

            return Response(serializer.data)
           
        
        else:
            pass
    
        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)















class IsSuperUser(APIView):

    def get(self, request):

        try:
            account = getAccount(request)
            return Response(account.isSuperUser)
        except:
            pass

        return Response(False)

    def post(self, request):
        pass

















class LocationView(APIView):

    def get(self, request):

        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data)

    def post(self, request):
        
        name = request.POST.get("name","")

        try:

            locationExist = Location.objects.get(name = name)

            error_message = 'Location with this name already exist'
            err = {
                'error_message' : error_message
            }
            serializer = ErrorCheckSerializer( err, many=False)
            return Response(serializer.data)

        except:

            location = Location()
            location.name = name
            location.save()

            locations = Location.objects.all()
            serializer = LocationSerializer(locations, many=True)

            return Response(serializer.data)



        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
















class EditLocation(APIView):

    def get(self, request):
        pass

    def post(self, request, id):

        name = request.POST.get("name", "")

        try:
            location = Location.objects.get(id = id)
            location.name = name
            location.save()

            serializer = LocationSerializer(location, many=False)
            return Response(serializer.data)
        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)














class DeleteLocation(APIView):

    def get(self, request, id):

        try:
            location = Location.objects.get(id = id)
            location.delete()

            code = 11
            success = {
                'code' : code
            }
            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass
        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request, id):
        pass
















class CategoryView(APIView):

    def get(self, request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


    def post(self, request):
        
        name = request.POST.get("name","")
        try:

            categoryExist = Category.objects.get(name = name)

            error_message = 'Category with this name already exist'
            err = {
                'error_message' : error_message
            }
            serializer = ErrorCheckSerializer( err, many=False)
            return Response(serializer.data)

        except:

            category = Category()
            category.name = name
            category.save()

            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)

            return Response(serializer.data)



        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


















class EditCategory(APIView):

    def get(self, request):
        pass

    def post(self, request, id):

        name = request.POST.get("name", "")

        try:
            category = Category.objects.get(id = id)
            category.name = name
            category.save()

            serializer = CategorySerializer(category, many=False)
            return Response(serializer.data)
        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)















class DeleteCategory(APIView):

    def get(self, request, id):

        try:
            category = Category.objects.get(id = id)
            category.delete()

            code = 11
            success = {
                'code' : code
            }
            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass
        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request, id):
        pass













class ImpactView(APIView):

    def get(self, request):

        impacts = Impact.objects.all()
        serializer = ImpactSerializer(impacts, many=True)

        return Response(serializer.data)

    def post(self, request):
        
        name = request.POST.get("name","")
        try:

            impactExist = Impact.objects.get(name = name)

            error_message = 'Impact with this name already exist'
            err = {
                'error_message' : error_message
            }
            serializer = ErrorCheckSerializer( err, many=False)
            return Response(serializer.data)

        except:

            impact = Impact()
            impact.name = name
            impact.save()

            impact = Impact.objects.all()
            serializer = ImpactSerializer(impact, many=True)

            return Response(serializer.data)



        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
















class EditImpact(APIView):

    def get(self, request):
        pass

    def post(self, request, id):

        name = request.POST.get("name", "")

        try:
            impact = Impact.objects.get(id = id)
            impact.name = name
            impact.save()

            serializer = ImpactSerializer(impact, many=False)
            return Response(serializer.data)
        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


















class DeleteImpact(APIView):

    def get(self, request, id):

        try:
            impact = Impact.objects.get(id = id)
            impact.delete()

            code = 11
            success = {
                'code' : code
            }
            serializer = SuccessCodeSerializer(success, many = False)
            return Response(serializer.data)

        except:
            pass
        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request, id):
        pass




















class ReportView(APIView):

    def get(self, request):
        
        account = getAccount(request)

        try:
            report = Report.objects.filter(account = account)
            
            bucket = []
            for item in report:

                reporter_name = account.name

                if item.reportType:
                    report_type = 'Positive'
                else:
                    report_type = 'Negative'
                
                location = Location.objects.get(id = item.location_id)
                report_location = location.name

                impact = Impact.objects.get(id = item.impact_id)
                report_impact = impact.name

                category = Category.objects.get(id = item.category_id)
                incident_category = category.name 

                incident_description = item.description
                report_deed = item.deed
                date = item.date

                buffer = {
                    'reporter_name': reporter_name,
                    'report_type': report_type,
                    'report_location': report_location,
                    'report_impact': report_impact,
                    'incident_category': incident_category,
                    'incident_description': incident_description,
                    'report_deed': item.deed,
                    'report_date': item.report_date,
                    'date': item.date
                }

                bucket.append(buffer)

            
            serializer = ReportSerializer(bucket, many=True)
            return Response(serializer.data)


        except:
            pass

        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)



    def post(self, request):
        
        account = getAccount(request)

        try:
            report_type = request.POST.get("type","")
            location = request.POST.get("location","")
            impact = request.POST.get("impact","")
            category = request.POST.get("category","")
            description = request.POST.get("description","")
            deed = request.POST.get("deed","")
            report_date = request.POST.get("date","")

            category = Category.objects.get(id = category)
            location = Location.objects.get(id = location)
            impact = Impact.objects.get(id = impact)

            if report_type == '1':
                report_type = True
            
            else:
                report_type = False

            report = Report()
            report.account = account
            report.category = category
            report.location = location
            report.impact = impact
            report.reportType = report_type
            report.description = description
            report.deed = deed
            report_date = report_date
            report.save()


            report = Report.objects.filter(account = account)
            bucket = []
            for item in report:

                reporter_name = account.name

                if item.reportType:
                    report_type = 'Positive'
                else:
                    report_type = 'Negative'
                
                location = Location.objects.get(id = item.location_id)
                report_location = location.name

                impact = Impact.objects.get(id = item.impact_id)
                report_impact = impact.name

                category = Category.objects.get(id = item.category_id)
                incident_category = category.name 

                incident_description = item.description
                report_deed = item.deed
                date = item.date

                buffer = {
                    'reporter_name': reporter_name,
                    'report_type': report_type,
                    'report_location': report_location,
                    'report_impact': report_impact,
                    'incident_category': incident_category,
                    'incident_description': incident_description,
                    'report_deed': item.deed,
                    'report_date': item.report_date,
                    'date': item.date
                }

                bucket.append(buffer)

            
            serializer = ReportSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry could not complete process, login and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)




















class ReportTypeAggregate(APIView):

    def get(self, request):

        try:
            positive = Report.objects.filter(reportType = 1).count()
            negative = Report.objects.filter(reportType = 0).count()

            bucket = {
                'positive': positive,
                'negative': negative
            }

            serializer = ReportTypeAggregateSerializer(bucket, many = False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        
        start_date = request.POST.get("start_date","")
        end_date = request.POST.get("end_date","")

        try :
            positive = Report.objects.filter(reportType = 1,  report_date__gt = start_date, report_date__lt = end_date).count()
            negative = Report.objects.filter(reportType = 0,  report_date__gt = start_date, report_date__lt = end_date).count()

            bucket = {
                'positive': positive,
                'negative': negative
            }

            serializer = ReportTypeAggregateSerializer(bucket, many = False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)




















class LocationAggregate(APIView):

    def get(self, request):

        try:
            locations = Location.objects.all()

            bucket = []
            for item in locations:
                value = Report.objects.filter(location = item.id).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        
        start_date = request.POST.get("start_date","")
        end_date = request.POST.get("end_date","")


        try:
            locations = Location.objects.all()

            bucket = []
            for item in locations:
                value = Report.objects.filter(location = item.id, report_date__gt = start_date, report_date__lt = end_date).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


















class ImpactAggregate(APIView):

    def get(self, request):

        try:
            impactlist = Impact.objects.all()

            bucket = []
            for item in impactlist:
                value = Report.objects.filter(impact = item.id).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        
        start_date = request.POST.get("start_date","")
        end_date = request.POST.get("end_date","")

        try:
            impactlist = Impact.objects.all()

            bucket = []
            for item in impactlist:
                value = Report.objects.filter(impact = item.id, report_date__gt = start_date, report_date__lt = end_date).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)


















class CategoryAggregate(APIView):

    def get(self, request):

        try:
            categorylist = Category.objects.all()

            bucket = []
            for item in categorylist:
                value = Report.objects.filter(category = item.id).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        
        start_date = request.POST.get("start_date","")
        end_date = request.POST.get("end_date","")


        try:
            categorylist = Category.objects.all()

            bucket = []
            for item in categorylist:
                value = Report.objects.filter(category = item.id, report_date__gt = start_date, report_date__lt = end_date).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)





















class UserAggregate(APIView):

    def get(self, request):

        try:
            accountlist = Account.objects.all()

            bucket = []
            for item in accountlist:
                value = Report.objects.filter(account = item.id).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        
        start_date = request.POST.get("start_date","")
        end_date = request.POST.get("end_date","")

        try :
            accountlist = Account.objects.all()

            bucket = []
            for item in accountlist:
                value = Report.objects.filter(account = item.id, report_date__gt = start_date, report_date__lt = end_date).count()

                buffer = {
                    'name': item.name,
                    'value': value
                }

                bucket.append(buffer)

            serializer = AggregateSerializer(bucket, many = True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

















class ReportAggregate(APIView):

    def get(self, request):
        
        account = getAccount(request)

        try:
            report = Report.objects.all()
            
            bucket = []
            for item in report:

                if item.reportType:
                    report_type = 'Positive'
                else:
                    report_type = 'Negative'
                
                user = Account.objects.get(id = item.account_id)
                reporter_name = user.name

                location = Location.objects.get(id = item.location_id)
                report_location = location.name

                impact = Impact.objects.get(id = item.impact_id)
                report_impact = impact.name

                category = Category.objects.get(id = item.category_id)
                incident_category = category.name 

                incident_description = item.description
                report_deed = item.deed
                date = item.date

                buffer = {
                    'reporter_name': reporter_name,
                    'report_type': report_type,
                    'report_location': report_location,
                    'report_impact': report_impact,
                    'incident_category': incident_category,
                    'incident_description': incident_description,
                    'report_deed': item.deed,
                    'report_date': item.report_date,
                    'date': item.date
                }

                bucket.append(buffer)

            
            serializer = ReportSerializer(bucket, many=True)
            return Response(serializer.data)


        except:
            pass

        error_message = 'Sorry could not complete process, reload page and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request):
        pass


















class SuperUserSort(APIView):

    def get(self, request):
        pass

    def post(self, request):
        

        try:
            report_type = request.POST.get("type","")
            location = request.POST.get("location","")
            impact = request.POST.get("impact","")
            category = request.POST.get("category","")
            report_date = request.POST.get("date","")

            categoryAll = False
            locationAll = False
            impactAll = False
            typeAll = False
            dateAll = False

            if category == '999':
                categoryAll = True
            else:
                category = Category.objects.get(id = category)
            
            if location == '999':
                locationAll = True
            else: 
                location = Location.objects.get(id = location)

            if impact == '999':
                impactAll = True
            else:
                impact = Impact.objects.get(id = impact)

            if report_date == '999':
                dateAll = True
            else:
                pass

            

            if report_type == '999':
                typeAll = True

            else:
                if report_type == '1':
                    report_type = True
                
                else:
                    report_type = False

            if (not categoryAll) and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, location = location, impact = impact, category = category)


            #Category Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(reportType = report_type, location = location, impact = impact, report_date__gt = report_date)
            elif (not categoryAll) and (not locationAll) and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(category = category, location = location, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(category = category, location = location)
            elif (not categoryAll) and locationAll and impactAll and dateAll and typeAll:
                report = Report.objects.filter(category = category)



            #Location Priority Sort
            elif (not categoryAll) and (not locationAll) and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(location = location, category = category, impact = impact, report_date__gt = report_date)
            elif (not categoryAll) and (not locationAll) and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(location = location, category = category, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(location = location, category = category)
            elif categoryAll and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(location = location)
            

            
            #Impact Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, impact = impact, location = location, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, impact = impact, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(impact = impact, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(impact = impact)
            


            #Date Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, impact = impact, location = location, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(impact = impact, reportType = report_type, report_date__gt = report_date)
            elif categoryAll and locationAll and impactAll and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, report_date__gt = report_date)
            elif categoryAll and locationAll and impactAll and (not dateAll) and typeAll:
                report = Report.objects.filter(report_date__gt = report_date)

            


            #Type Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, impact = impact, location = location)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and (not dateAll) and (not typeAll):
                report = Report.objects.filter(reportType = report_type)
            elif categoryAll and locationAll and impactAll and dateAll and (not typeAll):
                report = Report.objects.filter(reportType = report_type)


            else:
                report = Report.objects.all()

            #End of Priority Sort
            
            bucket = []
            for item in report:

                user = Account.objects.get(id = item.account_id)
                reporter_name = user.name

                if item.reportType:
                    report_type = 'Positive'
                else:
                    report_type = 'Negative'
                
                location = Location.objects.get(id = item.location_id)
                report_location = location.name

                impact = Impact.objects.get(id = item.impact_id)
                report_impact = impact.name

                category = Category.objects.get(id = item.category_id)
                incident_category = category.name 

                incident_description = item.description
                report_deed = item.deed
                date = item.date

                buffer = {
                    'reporter_name': reporter_name,
                    'report_type': report_type,
                    'report_location': report_location,
                    'report_impact': report_impact,
                    'incident_category': incident_category,
                    'incident_description': incident_description,
                    'report_deed': item.deed,
                    'report_date': item.report_date,
                    'date': item.date
                }

                bucket.append(buffer)

            
            serializer = ReportSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry could not complete process, login and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)
























class SortView(APIView):

    def get(self, request):
        pass

    def post(self, request):
        
        account = getAccount(request)

        try :
            report_type = request.POST.get("type","")
            location = request.POST.get("location","")
            impact = request.POST.get("impact","")
            category = request.POST.get("category","")
            report_date = request.POST.get("date","")

            categoryAll = False
            locationAll = False
            impactAll = False
            typeAll = False
            dateAll = False

            if category == '999':
                categoryAll = True
            else:
                category = Category.objects.get(id = category)
            
            if location == '999':
                locationAll = True
            else: 
                location = Location.objects.get(id = location)

            if impact == '999':
                impactAll = True
            else:
                impact = Impact.objects.get(id = impact)

            if report_date == '999':
                dateAll = True
            else:
                pass

            

            if report_type == '999':
                typeAll = True

            else:
                if report_type == '1':
                    report_type = True
                
                else:
                    report_type = False

            if (not categoryAll) and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, location = location, impact = impact, category = category)


            #Category Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(account = account, reportType = report_type, location = location, impact = impact, report_date__gt = report_date)
            elif (not categoryAll) and (not locationAll) and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(account = account, category = category, location = location, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(account = account, category = category, location = location)
            elif (not categoryAll) and locationAll and impactAll and dateAll and typeAll:
                report = Report.objects.filter(account = account, category = category)



            #Location Priority Sort
            elif (not categoryAll) and (not locationAll) and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(account = account, location = location, category = category, impact = impact, report_date__gt = report_date)
            elif (not categoryAll) and (not locationAll) and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(account = account, location = location, category = category, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(account = account, location = location, category = category)
            elif categoryAll and (not locationAll) and impactAll and dateAll and typeAll:
                report = Report.objects.filter(account = account, location = location)
            

            
            #Impact Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, impact = impact, location = location, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, impact = impact, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and typeAll:
                report = Report.objects.filter(account = account, impact = impact, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and dateAll and typeAll:
                report = Report.objects.filter(account = account, impact = impact)
            


            #Date Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, impact = impact, location = location, report_date__gt = report_date)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, impact = impact, reportType = report_type, report_date__gt = report_date)
            elif categoryAll and locationAll and impactAll and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, report_date__gt = report_date)
            elif categoryAll and locationAll and impactAll and (not dateAll) and typeAll:
                report = Report.objects.filter(account = account, report_date__gt = report_date)

            


            #Type Priority Sort
            elif categoryAll and (not locationAll) and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, impact = impact, location = location)
            elif categoryAll and locationAll and (not impactAll) and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type, impact = impact)
            elif (not categoryAll) and (not locationAll) and impactAll and (not dateAll) and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type)
            elif categoryAll and locationAll and impactAll and dateAll and (not typeAll):
                report = Report.objects.filter(account = account, reportType = report_type)


            else:
                report = Report.objects.filter(account = account)
            
            bucket = []
            for item in report:

                reporter_name = account.name

                if item.reportType:
                    report_type = 'Positive'
                else:
                    report_type = 'Negative'
                
                location = Location.objects.get(id = item.location_id)
                report_location = location.name

                impact = Impact.objects.get(id = item.impact_id)
                report_impact = impact.name

                category = Category.objects.get(id = item.category_id)
                incident_category = category.name 

                incident_description = item.description
                report_deed = item.deed
                date = item.date

                buffer = {
                    'reporter_name': reporter_name,
                    'report_type': report_type,
                    'report_location': report_location,
                    'report_impact': report_impact,
                    'incident_category': incident_category,
                    'incident_description': incident_description,
                    'report_deed': item.deed,
                    'report_date': item.report_date,
                    'date': item.date
                }

                bucket.append(buffer)

            
            serializer = ReportSerializer(bucket, many=True)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry could not complete process, login and try again'
        err = {
            'error_message' : error_message
        }
        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)























class MyReportAggregate(APIView):

    def get(self, request):

        try:
            account = getAccount(request)
            myReport = Report.objects.filter(account = account).count()
            totalReport = Report.objects.all().count()

            bucket = {
                'myReport': myReport,
                'totalReport': totalReport
            }

            serializer = MyReportAggregateSerializer(bucket, many = False)
            return Response(serializer.data)

        except:
            pass

        error_message = 'Sorry something broke, try again'
        err = {
            'error_message' : error_message
        }

        serializer = ErrorCheckSerializer( err, many=False)
        return Response(serializer.data)

    def post(self, request, id):
        pass






