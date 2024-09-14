from django.http import JsonResponse
from highrise_app.models import CorpFormData, EmpSetTarget, Members, FollowUpData, Sagemitra, HighRiseData, Target, CorporatesList, CorporateType, Interested_localities
from highrise_app.models import HomeVisit, IpData, AdmissionData, EventAcc, SageMitraList, EventType, SiteVisit, Source, States, City
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from datetime import datetime
from django.db.models import Q,  Count
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


import base64
from django.core.files.base import ContentFile
from django.utils import timezone



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def Dashboard(request, username):
    try:
       
        today_date = datetime.now().date()
        first_date = datetime.now().date().replace(day=1).strftime("%Y-%m-%d")
        month = timezone.now().strftime("%B")
        year = timezone.now().year
      
        userData = Members.objects.filter(member_name=username).values('id').first()
        if not userData:
            return JsonResponse({'error': 'User not found'}, status=404)

        user_id = userData['id']
        

        target_values = EmpSetTarget.objects.filter(Q(Employee_id=user_id) & Q(month=month) & Q(year=year)).values()
     
        corpo_solo = CorpFormData.objects.filter(Q(name=username) & Q(visit_date__range=(first_date, today_date))).count()

        corporate = CorpFormData.objects.filter(Q(visit_type='team') & Q(visit_date__range=(first_date, today_date)))
        team_corporate_visit_count = 0
        for visit in corporate:
            if visit.cofel_name:
                co_fellows = [name.strip() for name in visit.cofel_name.split(',')]
                if username in co_fellows:
                    team_corporate_visit_count += 1

        total_corp_visit = corpo_solo + team_corporate_visit_count
        total_followUP = FollowUpData.objects.filter(Employee_Name=username, FollowUp_Date__range=(first_date, today_date)).count()
        total_SM_FW = Sagemitra.objects.filter(uname=username, followUp_date__range=(first_date, today_date)).count()
        total_ip = IpData.objects.filter(name_id=user_id, date__range=(first_date, today_date)).count()
        total_admission = AdmissionData.objects.filter(name_id=user_id, date__range=(first_date, today_date)).count()
        total_event = EventAcc.objects.filter(name=username, start_date__range=(first_date, today_date)).count()
        # total_site_visit = FollowUpData.objects.filter(Employee_Name=username, FollowUp_Date__range=(first_date, today_date),EnquiryStage='Site Visit - Done').count()    

        # direct_site_visit = SiteVisit.objects.filter(Q(Q(sales_name = member['member_name']) & Q(Visit_Date__range = (start_date, end_date)) & Q(visit_type = 'direct'))).count()
        # direct_site_visit_2 = SiteVisit.objects.filter(Q(Q(reference = member['member_name']) & Q(Visit_Date__range = (start_date, end_date)) & Q(visit_type = 'indirect'))).count()
        # total_direct_site = direct_site_visit + direct_site_visit_2
        total_site_visit = SiteVisit.objects.filter(Q(Q(sales_name = username) & Q(Visit_Date__range = (first_date, today_date))) | Q(reference = username)).count()  
        count_data = HighRiseData.objects.filter(HandledByEmployee=username)
        panding_FW = count_data.filter(Next_FollowUp1__startswith=today_date).count()
        solo_home_visit = HomeVisit.objects.filter(Q(name=username) & Q(date__range=(first_date, today_date))).count()
        home_visits = HomeVisit.objects.filter(Q(visit_type='team') & Q(date__range=(first_date, today_date)))

        team_home_visit_count = 0
        for visit in home_visits:
            if visit.co_fellow:
                co_fellows = [name.strip() for name in visit.co_fellow.split(',')]
                if username in co_fellows:
                    team_home_visit_count += 1
        total_home_visit = solo_home_visit + team_home_visit_count
        

        data = {
            'targets': list(target_values),
            'total': {
                'total_corp_visit': total_corp_visit,
                'total_followUP': total_followUP,
                'total_SM_FW': total_SM_FW,
                'total_panding_FW': panding_FW,
                'total_home_visit': total_home_visit,
                'total_ip': total_ip,
                'total_admission': total_admission,
                'total_event': total_event,
                'total_site_visit': total_site_visit,
            }
        }
      
        return JsonResponse(data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=200)




@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    if request.method == "POST":
        username = request.data.get('username')
        password = request.data.get('password')
        

        user = authenticate(username=username, password=password)
   
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'first_name': user.first_name,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
         
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_200_OK)
    else:
      
        return Response({'error': 'Method not allowed'}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_Target(request, username):
    current_month = datetime.now().strftime("%B")
    
    if request.method == 'GET':
        try:
            employee = Members.objects.filter(member_name=username).values_list('id', flat=True)
            existing_entries = EmpSetTarget.objects.filter(Employee_id__in=employee, month=current_month).values()
            
            if existing_entries.exists():
                data = list(existing_entries)              
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No valid target entries found for the current month.'}, status=status.HTTP_200_OK)
        except Members.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_200_OK)
        



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Set_Target(request, username):
    if request.method == 'POST':              
        try:            
            employee_name = username
            year = request.data.get('year')
            month = request.data.get('month')
            booking = request.data.get('booking')
            corporate = request.data.get('corporate_visit')
            followup = request.data.get('followup')
            homevisit = request.data.get('home_visit')
            sm_mitra = request.data.get('sm_followup')
            sitevisit = request.data.get('site_visit')
            admission = request.data.get('admission')
            ip = request.data.get('ip')
            
            employee = Members.objects.get(member_name=employee_name)
            
            existing_entry = EmpSetTarget.objects.filter(Employee=employee, month=month).first()
            target_values = {
                1: booking,
                2: corporate,
                3: followup,
                4: homevisit,
                5: sm_mitra,
                6: sitevisit,
                7: admission,
                8: ip
            }
            
            if existing_entry and existing_entry.stage == 1:
                try:
                    for target_id, target_value in target_values.items():
                        if target_value:
                            target_instance = Target.objects.get(id=target_id)
                            set_target = EmpSetTarget.objects.filter(
                                Employee=employee,
                                year=year,
                                month=month,
                                Target=target_instance
                            ).first()
                            if set_target:
                                set_target.target = target_value
                                set_target.stage = 2
                                set_target.save()
                                
                            else:
                                return Response({'error': f'Entry for target {target_id} not found.'}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'error': 'Failed to update targets.'}, status=status.HTTP_200_OK)

            elif existing_entry and existing_entry.stage == 2:
               
                return Response({'error': 'You have already updated the target.'}, status=status.HTTP_200_OK)
            else:
                
                try:
                    for target_id, target_value in target_values.items():
                        if target_value:
                            target_instance = Target.objects.get(id=target_id)
                            EmpSetTarget.objects.create(
                                Employee=employee,
                                year=year,
                                month=month,
                                Target=target_instance,
                                target=target_value,
                                stage=1
                            )
                    return Response({'success': 'Your entry is saved (Your 1 Chance is left Now you can edit your target one more time only)'})
                except Exception as e:
                    return Response({'error': 'Failed to set targets.'}, status=status.HTTP_200_OK)

            return Response({'success': 'Targets set successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
        



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Data(request):
    corporate_list = CorporatesList.objects.values_list('corpo_name', 'corporate_type_id').order_by('corpo_name')
    corporate_type = CorporateType.objects.values_list('corpo_type', 'id').order_by('corpo_type')
    members = Members.objects.filter(status=1).values_list('member_name', flat=True).order_by('member_name')
    sage_mitra_list = SageMitraList.objects.values_list('sm_name', 'sm_ph').order_by('sm_name')
    event_type_list = EventType.objects.values_list('event_type', flat=True).order_by('event_type')
    interested_localities = Interested_localities.objects.values_list('localities', flat=True).order_by('localities')
    source =  Source.objects.values_list('name', 'id', 'source_id').order_by('name')
    state_location = States.objects.filter(country_id = 101).values_list('name', 'id').order_by('name')
    data = {
        'corporate_list': list(corporate_list),
        'corporate_type': list(corporate_type),
        'members': list(members),
        'sage_mitra_list': list(sage_mitra_list),
        'event_type_list': list(event_type_list),
        'interested_localities': list(interested_localities),
        'source' : list(source),
        'states_location' : list(state_location),
    }
    return Response(data)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def CorporateName(request):
    corp_id = request.data.get('corporate_id')
    if corp_id:
        corpo = CorporatesList.objects.filter(corporate_type_id = corp_id).values_list('corpo_name', flat=True).order_by('corpo_name')
        data = list(corpo)
    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CityData(request):
    if request.method == 'POST':
        stateId = request.data.get('stateId')
        data = City.objects.filter(state_id = stateId).values_list('name', flat=True).order_by('name')
        cities = list(data)
        return Response({'cities': cities}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def CorporateForm(request):
    
#     if request.method == 'POST':
#         try:
           
#             name =  request.data.get('name')           
#             corp_type = request.data.get('corp_type')
#             corp_name = request.data.get('corp_name')
#             meet_person = request.data.get('meet_person')
#             presentation = request.data.get('presentation')
#             today_date = datetime.now()
#             nxt_pre_date = request.data.get('nxt_date')
#             reason = request.data.get('reason')
#             key_person = request.data.get('key_person')
#             key_person_contact = request.data.get('key_person_contact')
#             key_person2 = request.data.get('key_person2')
#             key_person_contact2 = request.data.get('key_person_contact2')
#             data_collect = request.data.get('data_collect')
#             visit_type = request.data.get('visit_type')
#             location = request.data.get('location')
#             lat_long = request.data.get('lat_long')
#             # image = request.FILES.get('corporateVisitImage')
#             image = request.data.get('image') 
#             num_attend = request.data.get('num_attend') 
#             # print('===========', image)
#             imgstr = image['base64']
            
#             team_members = request.data.get('co_name')
#             if isinstance(team_members, str):
#                 team_members = team_members.split(',')
#             elif not isinstance(team_members, list):
#                 team_members = []

#             # Validate and process dates
#             # try:
#             #     visit_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#             # except (ValueError, TypeError):
#             #     return Response({'error': 'Invalid date format. Please enter the date in YYYY-MM-DD format.'}, status=status.HTTP_200_OK)

#             nxt_date = None
#             if nxt_pre_date:
#                 try:
#                     nxt_date = datetime.strptime(nxt_pre_date, '%Y-%m-%d').date()
#                 except (ValueError, TypeError):
#                     return Response({'error': 'Invalid next date format. Please enter the date in YYYY-MM-DD format.'}, status=status.HTTP_200_OK)

#             # Validate image
#             if not image:
#                 return Response({'error': 'No image file provided.'}, status=status.HTTP_200_OK)

#             current_time = datetime.now().strftime('%Y%m%d%H%M%S')
#             # image_name, image_ext = os.path.splitext(image.name)
#             # new_filename = f"{slugify(name)}_{date_str}_{slugify(corp_name)}_{current_time}{image_ext}"
#             # image.name = new_filename
#             ext = image['fileName'].split('.')[-1]
#             new_filename = f"{slugify(name)}_{today_date}_{slugify(corp_name)}_{slugify(current_time)}.{ext}"
#             image_content = ContentFile(base64.b64decode(imgstr), name=new_filename)
        
#             # Handle team members
#             co_names_str = ','.join(team_members) if team_members else None
#             username = CorpFormData.objects.filter(Q(key_person_contact = key_person_contact) & Q(name = name)).count()
#             if username > 0:
#                 revisit = 1 + username                                                         
#             else:
#                 revisit = 1

#             # Save to model
#             corp_form_data = CorpFormData.objects.create(
#                 lat_long= lat_long,
#                 key_person2=key_person2,
#                 key_person_contact2=key_person_contact2,
#                 name=name,
#                 corp_name=corp_name,
#                 corp_type=corp_type,
#                 meet_person=meet_person,
#                 presentation=presentation,
#                 cofel_name=co_names_str,
#                 visit_date=today_date,
#                 reason=reason,
#                 nxt_pre_date=nxt_date,
#                 key_person=key_person,
#                 images=image_content,
#                 data_collect=data_collect,
#                 key_person_contact=key_person_contact,
#                 visit_type=visit_type,
#                 location=location,
#                 num_attend = num_attend,
#                 revisit=revisit
#             )
#             corp_form_data.save()
#             return Response({'success': 'Your entry has been saved'}, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_200_OK)


#     return Response(status=status.HTTP_400_BAD_REQUEST)



from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CorporateForm(request):
    
    if request.method == 'POST':
        try:
            # Collecting the form data
            name = request.data.get('name')
            corp_type = request.data.get('corp_type')
            corp_name = request.data.get('corp_name')
            meet_person = request.data.get('meet_person')
            presentation = request.data.get('presentation')
            today_date = datetime.now()
            nxt_pre_date = request.data.get('nxt_date')
            reason = request.data.get('reason')
            key_person = request.data.get('key_person')
            key_person_contact = request.data.get('key_person_contact')
            key_person2 = request.data.get('key_person2')
            key_person_contact2 = request.data.get('key_person_contact2')
            data_collect = request.data.get('data_collect')
            visit_type = request.data.get('visit_type')
            location = request.data.get('location')
            lat_long = request.data.get('lat_long')
            image = request.data.get('image') 
            num_attend = request.data.get('num_attend')

            imgstr = image['base64']

            team_members = request.data.get('co_name')
            if isinstance(team_members, str):
                team_members = team_members.split(',')
            elif not isinstance(team_members, list):
                team_members = []

            # Validate and process dates
            nxt_date = None
            if nxt_pre_date:
                try:
                    nxt_date = datetime.strptime(nxt_pre_date, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return Response({'error': 'Invalid next date format. Please enter the date in YYYY-MM-DD format.'}, status=status.HTTP_200_OK)

            # Validate image
            if not image:
                return Response({'error': 'No image file provided.'}, status=status.HTTP_200_OK)

            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = 'webp'  # Set the file extension to WebP
            new_filename = f"{slugify(name)}_{today_date}_{slugify(corp_name)}_{slugify(current_time)}.{ext}"

            # Decode the base64 image and convert it to WebP using Pillow
            image_data = base64.b64decode(imgstr)
            image_content = BytesIO(image_data)
            
            # Convert image to WebP using Pillow
            with Image.open(image_content) as img:
                # img.thumbnail((800, 600))
                webp_image_io = BytesIO()
                img.save(webp_image_io, format='WEBP', quality=85)
                webp_image_io.seek(0)

                # Create a ContentFile for the WebP image
                image_content_webp = ContentFile(webp_image_io.read(), name=new_filename)

            # Handle team members
            co_names_str = ','.join(team_members) if team_members else None
            username = CorpFormData.objects.filter(Q(key_person_contact=key_person_contact) & Q(name=name)).count()
            revisit = 1 + username if username > 0 else 1

            # Save to model
            corp_form_data = CorpFormData.objects.create(
                lat_long=lat_long,
                key_person2=key_person2,
                key_person_contact2=key_person_contact2,
                name=name,
                corp_name=corp_name,
                corp_type=corp_type,
                meet_person=meet_person,
                presentation=presentation,
                cofel_name=co_names_str,
                visit_date=today_date,
                reason=reason,
                nxt_pre_date=nxt_date,
                key_person=key_person,
                images=image_content_webp,  # Save the WebP image
                data_collect=data_collect,
                key_person_contact=key_person_contact,
                visit_type=visit_type,
                location=location,
                num_attend=num_attend,
                revisit=revisit
            )
            corp_form_data.save()

            return Response({'success': 'Your entry has been saved'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SageMitraForm(request):
    if request.method == 'POST':
        try:

            
            uname = request.data.get('username')
            sm_name = request.data.get('sm_name')
            today_date = datetime.now()  
            no_leads = request.data.get('no_leads')
            lead_detail = request.data.get('lead_Detail')
            sm_contact = request.data.get('sm_contact')
            new_sm_name = request.data.get('new_sm_name')
            new_sm_contact = request.data.get('new_sm_contact')
            # followup_date = datetime.strptime(date, '%Y-%m-%d').date()
            sub_date = timezone.now()
            
            if new_sm_name != '' and new_sm_contact != '':
                
                new_sm = SageMitraList.objects.create(
                    sm_name = new_sm_name,
                    sm_ph=new_sm_contact
                )
                new_sm.save()
            
                try:
                    sage_mitra = Sagemitra.objects.create(
                        new_sm_contact=new_sm_contact,
                        uname=uname,
                        SM_name=new_sm_name,
                        followUp_date=today_date,
                        No_leads=no_leads,
                        lead_detail=lead_detail,
                        new_sm_name=new_sm_name,
                        submission_date = sub_date,
                    )
                    sage_mitra.save()
                    success_message = 'SageMitra Detail Added'
                    return Response({'success':success_message}, status= status.HTTP_200_OK)
                except Exception as e:
                    error_message = 'Invalid input'
                    return Response({'error': error_message}, status=status.HTTP_200_OK)
            else:
                try:                
                    sage_mitra = Sagemitra.objects.create(
                        sm_contact=sm_contact,
                        uname=uname,
                        SM_name=sm_name,
                        followUp_date=today_date,
                        No_leads=no_leads,
                        lead_detail=lead_detail,
                        submission_date = sub_date,
                    )
                    sage_mitra.save()
                    success_message = 'SageMitra Detail Added'
                    return Response({'success': success_message}, status=status.HTTP_200_OK)
                except Exception as e:

                    error_message = 'Invalid input'
                    return Response({'error': error_message}, status=status.HTTP_200_OK)
        except Exception as e:
            print("========", e)
            return Response({'error': e})
    else:
        return Response({'error': 'Invalid Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def Home_Visit(request):
#     currentTime = datetime.now().strftime('%H-%M-%S')    
#     if request.method == 'POST':
#         try:       
#             name =  request.data.get('username')
#             customer_name = request.data.get('customer_name')
#             customer_contact = request.data.get('customer_contact')
#             Today_date =  datetime.now()
#             visit_details = request.data.get('visit_details')
#             Visit_location = request.data.get('Visit_location')
#             visit_type = request.data.get('visit_type')
#             image = request.data.get('image') 
#             lat_long = request.data.get('lat_long')
            
#             # print("====", lat_long['longitude'])

#             imgstr = image['base64']
            
#             username = HomeVisit.objects.filter(Q(C_ph = customer_contact) & Q(name = name)).count()
#             if username > 0:
#                 revisit = 1 + username                                                         
#             else:
#                 revisit = 1

        
#             if not image:
#                 return Response({'error': 'No image file provided.'}, status=status.HTTP_200_OK) 
            
#             ext = image['fileName'].split('.')[-1]
#             new_filename = f"{slugify(name)}_{date}_{slugify(Visit_location)}_{slugify(currentTime)}.{ext}"
#             image_content = ContentFile(base64.b64decode(imgstr), name=new_filename)
            
#             team_members = request.data.get('co_name')
            

#             if isinstance(team_members, str):
#                 team_members = team_members.split(',')
#             elif not isinstance(team_members, list):
#                 team_members = []
#             co_names_str = ','.join(team_members) if team_members else None

#             try:
#                 HomeVisit.objects.create(
#                     name=name,
#                     C_name=customer_name,
#                     C_ph=customer_contact,
#                     date=Today_date,
#                     detail=visit_details,
#                     Visit_location=Visit_location,
#                     images=image_content,
#                     co_fellow=co_names_str,
#                     visit_type=visit_type,
#                     lat_long= lat_long,
#                     revisit= revisit
#                 )
#                 return Response({'success': 'Home visit recorded successfully.'}, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error': 'Failed to save home visit.'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             print("=========", e)
#             return Response({'error': str(e)})
#     else:
#         return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Home_Visit(request):
    currentTime = datetime.now().strftime('%H-%M-%S')    
    if request.method == 'POST':
        try:       
            name = request.data.get('username')
            customer_name = request.data.get('customer_name')
            customer_contact = request.data.get('customer_contact')
            Today_date = datetime.now()
            visit_details = request.data.get('visit_details')
            Visit_location = request.data.get('Visit_location')
            visit_type = request.data.get('visit_type')
            image = request.data.get('image') 
            lat_long = request.data.get('lat_long')

            imgstr = image['base64']
            
            username = HomeVisit.objects.filter(Q(C_ph=customer_contact) & Q(name=name)).count()
            revisit = 1 + username if username > 0 else 1

            if not image:
                return Response({'error': 'No image file provided.'}, status=status.HTTP_200_OK)
            
            # Prepare WebP file extension
            ext = 'webp'
            new_filename = f"{slugify(name)}_{Today_date}_{slugify(Visit_location)}_{slugify(currentTime)}.{ext}"

            # Convert the base64 image to WebP using Pillow
            image_data = base64.b64decode(imgstr)
            image_content = BytesIO(image_data)
            
            # Convert image to WebP using Pillow
            with Image.open(image_content) as img:
                # img.thumbnail((500, 400))
                webp_image_io = BytesIO()
                img.save(webp_image_io, format='WEBP', quality=85)
                webp_image_io.seek(0)

                # Create a ContentFile for the WebP image
                image_content_webp = ContentFile(webp_image_io.read(), name=new_filename)

            # Handle team members
            team_members = request.data.get('co_name')
            if isinstance(team_members, str):
                team_members = team_members.split(',')
            elif not isinstance(team_members, list):
                team_members = []
            co_names_str = ','.join(team_members) if team_members else None


            try:
                data = HomeVisit.objects.create(
                    name=name,
                    C_name=customer_name,
                    C_ph=customer_contact,
                    date=Today_date,
                    detail=visit_details,
                    Visit_location=Visit_location,
                    images=image_content_webp, 
                    co_fellow=co_names_str,
                    visit_type=visit_type,
                    lat_long=lat_long,
                    revisit=revisit
                )
                data.save()
                return Response({'success': 'Home visit recorded successfully.'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Failed to save home visit.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EventForm(request):
    if request.method == 'POST':
      
        EventName = request.data.get('Event_name')
        name = request.data.get('username')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        Eventtype = request.data.get('Event_type')
        NumLeads = request.data.get('num_leads')
        event_details = request.data.get('event_details')
        num_attendees = request.data.get('num_attendees')
        
        
        try:         
            eventuser = EventAcc.objects.create(
                Event_name=EventName,
                name=name,
                start_date=start_date,
                end_date=end_date,
                type=Eventtype,
                num_attendees=num_attendees,
                num_lead=NumLeads,
                event_details=event_details,
            )
            eventuser.save()            
            return Response({'message': 'Event created successfully'}, status=status.HTTP_201_CREATED)
    
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
    
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AdmissonForm(request):
    if request.method == 'POST':
        name = request.data.get('username')
        today_date = date.today()   
        f_name = request.data.get('f_name')
        s_name = request.data.get('s_name')
        vertical = request.data.get('vertical')
        branch_class = request.data.get('branch_class')

        employee = Members.objects.get(member_name=name)
        
        try:
            user = AdmissionData.objects.create(
                name = employee,
                date = today_date,
                f_name = f_name,
                s_name = s_name,
                vertical = vertical,
                branch_class = branch_class,
            )
            user.save()
            return Response({'message': 'Admission Form Submitted'}, status=status.HTTP_201_CREATED)

        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)   
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def IpForm(request):
    if request.method == 'POST':
        name = request.data.get('username')
        today_date = datetime.now()
        p_name = request.data.get('p_name')
        key_person = request.data.get('key_person')
        employee = Members.objects.get(member_name=name)
        try:
            user = IpData.objects.create(
                name = name,
                date = today_date,
                patient_name = p_name,
                key_person = key_person,
            )
            user.save()
            return Response({'message': 'Ip Form Submitted'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)   
    




@api_view(['POST'])
@permission_classes([AllowAny])
def Forget_password(request):
    if request.method == 'POST':
        uname = request.data.get('username')
        current_password = request.data.get('current_password')
       
        if not uname or not current_password:
            message = 'Please provide both username and current password.'
            return Response({'error': message}, status=status.HTTP_200_OK)

        user = authenticate(request, username=uname, password=current_password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email, }
                }
            return Response({'success': 'User is valid', 'data': data}, status=status.HTTP_200_OK)
        else:
            message = 'Invalid username or current password.'
            return Response({'error': message}, status=status.HTTP_200_OK)

    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)   
    




from django.contrib.auth.models import User
@api_view(['POST'])
@permission_classes([AllowAny])
def Reset_password(request):
    if request.method == 'POST':
        
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password') 
        uname = request.data.get('username')  

        if password != confirm_password:
            message = 'Passwords do not match.'
            return Response({'error': message}, status=status.HTTP_200_OK)
        try:            
            user = User.objects.get(username=uname)
            user.password = make_password(password)
            user.save()
            success= 'Password updated successfully. Please log in.'
            return Response({'success': success}, status=status.HTTP_202_ACCEPTED )
        except User.DoesNotExist:
            message = 'User not found.'
            return Response({'error':message}, status=status.HTTP_200_OK)
      
    else:
        return Response({'error':'Method Not allowed'}, status= status.HTTP_405_METHOD_NOT_ALLOWED)
    

import random

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def SiteVisitFrom(request):
    
    if request.method == 'POST':  
        Customer_name = request.data.get('customer_name')
        customer_contact = request.data.get('customer_contact')
        email = request.data.get('email')
        dob_str  = request.data.get('DOB')
        marriage_anniversary_str  = request.data.get('marriage_anniversary')
        address = request.data.get('address')
        state = request.data.get('state')
        city = request.data.get('city')

        company = request.data.get('company')
        annual_income = request.data.get('annual_income')
        department = request.data.get('department')
        designation = request.data.get('designation')
        monthly_rent = request.data.get('monthly_rent')
        residential_status = request.data.get('residential_status')
        official_email = request.data.get('official_email')
        marital_status = request.data.get('marital_status')

        # visit_date_str  = request.data.get('date')
        customer_whatspp = request.data.get('customer_whatsapp')
        instagram = request.data.get('instagram')
        facebook = request.data.get('facebook')

        expected_possession  = request.data.get('expected_possession')
        interest = request.data.get('interested_location')
        accommodation = request.data.get('accommodation')
        purpose = request.data.get('purpose')
        Budget = request.data.get('Budget')
        sourceType = request.data.get('sourceType')
        source = request.data.get('source')
        Remark  = request.data.get('Remark')

        unique_id = random.randint(1, 999999)        
        customer_id = request.data.get('customer_id')
        sales_man = request.data.get('username')
        reference = request.data.get('member')
        visit_type = request.data.get('visit_type')
        lat_long = request.data.get('lat_long')
        site_location = request.data.get('siteLocation')
        username = SiteVisit.objects.filter(Customer_Contact_number = customer_contact).count()
        if username > 0:
            revisit = 1 + username                                                         
        else:
            revisit = 1
        try: 
            visit_date = datetime.now()
            # visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date() if visit_date_str else None
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
            marriage_anniversary = datetime.strptime(marriage_anniversary_str, '%Y-%m-%d').date() if marriage_anniversary_str else None
           
            
            
            if customer_id:     
               
                entry_exisit = SiteVisit.objects.filter(access_id=customer_id).first()
                if entry_exisit: 
                    entry_exisit.Customer_name = Customer_name
                    entry_exisit.Customer_Contact_number = customer_contact
                    entry_exisit.Email_id = email
                    entry_exisit.DOB = dob
                    entry_exisit.marriage_anniversary = marriage_anniversary
                    entry_exisit.Address = address
                    entry_exisit.state = state
                    entry_exisit.city = city

                    entry_exisit.Company = company
                    entry_exisit.Gross_Income = annual_income
                    entry_exisit.Department = department
                    entry_exisit.Designation = designation
                    entry_exisit.Monthly_rent = monthly_rent
                    entry_exisit.residential_status = residential_status
                    entry_exisit.official_mail = official_email
                    entry_exisit.marital_status = marital_status


                    entry_exisit.Customer_Whatspp_number = customer_whatspp
                    entry_exisit.Instagram = instagram
                    entry_exisit.Facebook_id = facebook

                    entry_exisit.Expected_possession = expected_possession
                    entry_exisit.Interest = interest
                    entry_exisit.accommodation = accommodation
                    entry_exisit.purpose = purpose
                    entry_exisit.Budget = Budget
                    entry_exisit.source = source
                    entry_exisit.source_type = sourceType
                    entry_exisit.Remark = Remark

                    entry_exisit.sales_name = sales_man
                    entry_exisit.reference = reference
                    entry_exisit.visit_type = visit_type
                    entry_exisit.site_location = site_location
                    entry_exisit.revisit = revisit


                    entry_exisit.save()
                    return JsonResponse({'success':'Site Visit Form submited successfully'}, status = status.HTTP_200_OK)
            
            else:
              
                data = SiteVisit.objects.create( sales_name = sales_man, Remark = Remark, reference= reference, visit_type = visit_type,
                    Customer_name = Customer_name, Customer_Contact_number = customer_contact, Customer_Whatspp_number = customer_whatspp,
                    Visit_Date = visit_date, Monthly_rent = monthly_rent, Address = address, Instagram = instagram, Email_id = email, Facebook_id = facebook, 
                    Company = company, Gross_Income = annual_income, Department = department, Designation = designation, DOB = dob,
                    marriage_anniversary = marriage_anniversary, Interest = interest, Budget = Budget, accommodation =accommodation, source= source,
                    Expected_possession = expected_possession, access_id = unique_id, official_mail = official_email,  state=state, city=city,source_type = sourceType, lat_long= lat_long, purpose= purpose, site_location = site_location, residential_status=residential_status
                    , marital_status= marital_status , revisit = revisit
                )        
                data.save()
                return JsonResponse({'success':'Site Visit Form submited successfully'}, status = status.HTTP_200_OK)
        
        except Exception as e:
            return JsonResponse({'error': e}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse(status = status.HTTP_400_BAD_REQUEST )



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def GetClientData(request):
    if request.method == 'POST':
        # CustomerId = request.data.get('customer_contact')
        CustomerId = request.data.get('customer_value') 
        home_contact = request.data.get('home_contact') 
        # print("===", home_contact)
        try:

            # FormData = SiteVisit.objects.filter(access_id = CustomerId).values()
            if CustomerId:
                FormData = SiteVisit.objects.filter(Q(Customer_Contact_number = CustomerId) | Q(access_id = CustomerId)).values()
                data = list(FormData)
            elif home_contact:
                data = HomeVisit.objects.filter(C_ph = home_contact).order_by('-id').values().first()
            # print("=============",data)
            return JsonResponse({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else :
        return JsonResponse({'error':'Id not Found'}, status=status.HTTP_400_BAD_REQUEST)
    
    
# @permission_classes([AllowAny])
# @api_view(['GET'])
# def FormData(request, username, form_id):
#     print("=================")

#     if request.method == 'GET':
#         print("=================", username, form_id)

#         if form_id == 'corporate':
#             todayDate = datetime.now().date
#             data = CorpFormData.objects.filter().all().values()
#             return Response({'data':data}, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_200_OK)
    

#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


from datetime import date
@api_view(['GET'])
@permission_classes([AllowAny])
def FormData(request, username, form_id):

    if request.method == 'GET': 
        try:
            dateFilter = request.GET.get('date')
            data = None
            currentMonth = None
            todayDate = None
            count = 0
            if dateFilter is not None:
                currentMonth = date.today().month  
                # currentMonth = 9  
            else:
                todayDate = date.today()    

         
            if currentMonth is not None:
             
                if form_id == 'corporate':                     
                    data = CorpFormData.objects.filter(Q(name = username) & Q(visit_date__month = currentMonth)).all().values()
                elif form_id == 'home':
                    data = []
                    # data = HomeVisit.objects.filter(Q(name = username) & Q(date__month = currentMonth)).all().values()
                    data_entry = (HomeVisit.objects.filter(Q(name=username) & Q(date__month = currentMonth))  
                            .values('C_name', 'C_ph').annotate(No_Visits=Count('C_ph')).order_by('-date')) 
                    data_cofellow_entry = HomeVisit.objects.filter(Q(date__month = currentMonth) & Q(visit_type='team')).values()
                    if data_cofellow_entry.exists():
                        for entry in data_cofellow_entry:
                            co_fellow = entry['co_fellow']
                            
                            if co_fellow == username:
                                
                                data.append({
                                    'C_name': entry['C_name'],
                                    'C_ph': entry['C_ph'],
                                    'record': {
                                        'detail': entry['detail'],
                                        'date': entry['date'],
                                        'visit_type': entry['visit_type'],
                                        'co_fellow': entry['co_fellow'],
                                        'Visit_location': entry['Visit_location']
                                    }
                                }) 

                    if data_entry.exists():                       
                       
                        for entry in data_entry:
                            C_ph = entry['C_ph']
                            
                            detailed_data = HomeVisit.objects.filter(
                                Q(name=username) & Q(date__month=currentMonth) & Q(C_ph=C_ph)).values('detail', 'date', 'visit_type', 'co_fellow', 'Visit_location').order_by('-date')

                            data.append({
                                # 'id' : entry['id'],
                                'C_name': entry['C_name'],
                                'C_ph': C_ph,                               
                                'record': list(detailed_data) 
                            })                       
                    
                    # print("=============", data)
                elif form_id == 'ip':
                    username = Members.objects.filter(member_name = username).values('id')
                    data = IpData.objects.filter(Q(name_id__in = username) & Q(date__month = currentMonth)).all().values()
                elif form_id == 'admission':
                    username = Members.objects.filter(member_name = username).values('id')
                    data = AdmissionData.objects.filter(Q(name_id__in = username) & Q(date__month = currentMonth)).all().values()
                elif form_id == 'sagemitra':
                    data = Sagemitra.objects.filter(Q(uname = username) & Q(followUp_date__month = currentMonth)).all().values()
                elif form_id == 'site':
                    data = SiteVisit.objects.filter(Q(sales_name = username) & Q(Visit_Date__month = currentMonth)).all().values()
                elif form_id == 'event':
                    data = EventAcc.objects.filter(Q(name = username) & Q(Q(start_date__month = currentMonth) | Q(end_date__month = currentMonth))).all().values()
           
            elif todayDate is not None:
              
                if form_id == 'corporate':                     
                    data = CorpFormData.objects.filter(Q(name = username) & Q(visit_date = todayDate)).all().values()
                    count = CorpFormData.objects.filter(Q(name = username) & Q(visit_date = todayDate)).count()
                elif form_id == 'home':
                    data = []
                    # data = HomeVisit.objects.filter(Q(name = username) & Q(date = todayDate)).all().values()
                    data_entry = (HomeVisit.objects.filter(Q(name=username) & Q(date = todayDate))  
                            .values('C_name', 'C_ph').annotate(No_Visits=Count('C_ph')).order_by('-date')) 
                    


                    data_cofellow_entry = HomeVisit.objects.filter(Q(date = todayDate) & Q(visit_type='team')).values()
                    if data_cofellow_entry.exists():
                        for entry in data_cofellow_entry:
                            co_fellow = entry['co_fellow']
                            
                            if co_fellow == username:
                                
                                data.append({
                                    'C_name': entry['C_name'],
                                    'C_ph': entry['C_ph'],
                                    'record': {
                                        'detail': entry['detail'],
                                        'date': entry['date'],
                                        'visit_type': entry['visit_type'],
                                        'co_fellow': entry['co_fellow'],
                                        'Visit_location': entry['Visit_location']
                                    }
                                }) 
                    
                    if data_entry.exists():
                        
                       
                        for entry in data_entry:
                            C_ph = entry['C_ph']
                            
                            detailed_data = HomeVisit.objects.filter(
                                Q(name=username) & Q(date = todayDate) & Q(C_ph=C_ph)
                            ).values('detail', 'date', 'visit_type', 'co_fellow', 'Visit_location').order_by('-date')

                            data.append({
                                # 'id' : entry['id'],
                                'C_name': entry['C_name'],
                                'C_ph': C_ph,                               
                                'record': list(detailed_data) 
                            }) 
                            
                    count = HomeVisit.objects.filter(Q(name = username) & Q(date = todayDate)).count()

                elif form_id == 'ip':
                    username = Members.objects.filter(member_name = username).values('id')
                    data = IpData.objects.filter(Q(name_id__in = username) & Q(date = todayDate)).all().values()
                    count = IpData.objects.filter(Q(name_id__in = username) & Q(date = todayDate)).count()

                elif form_id == 'admission':
                    username = Members.objects.filter(member_name = username).values('id')
                    data = AdmissionData.objects.filter(Q(name_id__in = username) & Q(date = todayDate)).all().values()
                    count = AdmissionData.objects.filter(Q(name_id__in = username) & Q(date = todayDate)).count()

                elif form_id == 'sagemitra':
                    data = Sagemitra.objects.filter(Q(uname = username) & Q(followUp_date = todayDate)).all().values()
                    count = Sagemitra.objects.filter(Q(uname = username) & Q(followUp_date = todayDate)).count()

                elif form_id == 'site':
                    data = SiteVisit.objects.filter(Q(sales_name = username) & Q(Visit_Date = todayDate)).all().values()
                    count = SiteVisit.objects.filter(Q(sales_name = username) & Q(Visit_Date = todayDate)).count()

                elif form_id == 'event':
                    data = EventAcc.objects.filter(Q(name = username) & Q(Q(start_date = todayDate) | Q(end_date = todayDate))).all().values()
                    count = EventAcc.objects.filter(Q(name = username) & Q(Q(start_date = todayDate) | Q(end_date = todayDate))).count()

            return Response({'data': data, 'count': count}, status=status.HTTP_200_OK)
        except Exception as e:
            print("=============", e)
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



