from datetime import date

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from .models import Chat, Feedback
from main_app.models import patient, doctor, diseaseinfo, consultation
from main_app.notifications import send_appointment_notifications

# Create your views here.



def post_feedback(request):
    
  if request.method == "POST":

      feedback = request.POST.get('feedback', None)
      if feedback != '':  
        f = Feedback(sender=request.user, feedback=feedback)
        f.save()        
        print(feedback)   

        try:
           if (request.user.patient.is_patient == True) :
              return HttpResponse("Feedback successfully sent.")
        except:
          pass
        if (request.user.doctor.is_doctor == True) :
           return HttpResponse("Feedback successfully sent.")

      else :
        return HttpResponse("Feedback field is empty   .")



def get_feedback(request):
    
    if request.method == "GET":

      obj = Feedback.objects.all()
      
      return redirect(request, 'consultation/chat_body.html',{"obj":obj})





#-----------------------------chatting system ---------------------------------------------------


# def post(request):
#     if request.method == "POST":
#         msg = request.POST.get('msgbox', None)

#         consultation_id = request.session['consultation_id'] 
#         consultation_obj = consultation.objects.get(id=consultation_id)

#         c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

#         #msg = c.user.username+": "+msg

#         if msg != '':            
#             c.save()
#             print("msg saved"+ msg )
#             return JsonResponse({ 'msg': msg })
#     else:
#         return HttpResponse('Request must be POST.')



# def messages(request):
#    if request.method == "GET":

#          consultation_id = request.session['consultation_id'] 

#          c = Chat.objects.filter(consultation_id=consultation_id)
#          return render(request, 'consultation/chat_body.html', {'chat': c})
#          return render(request, 'consultation/chat_body.html', {'chat': c})


def _get_patient_from_user(user):
    try:
        return user.patient
    except Exception:
        return None


def _get_last_prediction_reply(user):
    if not user.is_authenticated:
        return "Please sign in as a patient to see your last prediction."

    patient_obj = _get_patient_from_user(user)
    if patient_obj is None:
        return "Last prediction is available only for patient accounts."

    last_disease = (
        diseaseinfo.objects.filter(patient=patient_obj)
        .order_by("-id")
        .first()
    )

    if last_disease is None:
        return "I could not find any previous predictions for you."

    name = last_disease.diseasename
    confidence = str(last_disease.confidence)
    method = last_disease.prediction_method
    doctor_type = last_disease.consultdoctor

    parts = [
        "Your last prediction was " + name + ".",
        "Confidence: " + confidence + "%.",
    ]

    if method == "image":
        parts.append("This was predicted using the image scanner.")
    elif method == "symptoms":
        parts.append("This was predicted using the symptom checker.")

    if doctor_type:
        parts.append("Recommended specialist: " + doctor_type + ".")

    consultation_obj = (
        consultation.objects.filter(diseaseinfo=last_disease)
        .order_by("-consultation_date", "-id")
        .first()
    )

    link_html = ""
    if consultation_obj is not None:
        url = reverse("consultationview", args=[consultation_obj.id])
        link_html = ' <a href="' + url + '">Open related consultation</a>.'

    return " ".join(parts) + link_html


def _get_consultation_summary_reply(user):
    if not user.is_authenticated:
        return "Please sign in as a patient to see your consultations."

    patient_obj = _get_patient_from_user(user)
    if patient_obj is None:
        return "Consultation history is available only for patient accounts."

    consultations = (
        consultation.objects.filter(patient=patient_obj)
        .order_by("-consultation_date", "-id")[:3]
    )

    if not consultations:
        return "You do not have any consultations yet."

    lines = ["Here are your recent consultations:<ul>"]
    for c in consultations:
        doctor_name = c.doctor.name if c.doctor else "Doctor"
        date_text = (
            c.consultation_date.strftime("%Y-%m-%d")
            if c.consultation_date
            else "date not set"
        )
        status_text = c.status or "unknown"
        url = reverse("consultationview", args=[c.id])
        line_html = (
            '<li><a href="'
            + url
            + '">'
            + date_text
            + " - Dr. "
            + doctor_name
            + " ("
            + status_text
            + ")</a></li>"
        )
        lines.append(line_html)

    lines.append("</ul>")
    return " ".join(lines)


def _get_general_chatbot_reply(message, user):
    text = message.lower()

    if any(greeting in text for greeting in ["hi", "hello", "hey"]):
        if user.is_authenticated:
            name = ""
            try:
                if hasattr(user, "patient"):
                    name = user.patient.name
                elif hasattr(user, "doctor"):
                    name = "Dr. " + user.doctor.name
            except Exception:
                name = user.username

            if name:
                return "Hello, " + name + ". I can help you check disease features, view your recent results, and schedule appointments."

        return "Hello. I can help you understand this platform, view your recent results, and schedule appointments."

    if "symptom" in text or "disease" in text:
        return "To check a skin disease, go to the patient dashboard and open the symptom checker or image scanner. You can type 'book appointment' here to schedule an online consultation."

    if "appointment" in text or "schedule" in text or "book" in text:
        return "I can help you schedule an appointment. Say something like: Book an appointment with a dermatologist."

    if "help" in text or "what can you do" in text or "options" in text:
        return "You can ask me to book an appointment, show your last prediction, or list your recent consultations."

    return "I did not fully understand that. You can ask about disease checking or say you want to book an appointment."


@require_http_methods(["POST"])
def chatbot_message(request):
    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse({"reply": "Please type a message so I can help you."})

    state = request.session.get("chatbot_state") or {}
    mode = state.get("mode")
    step = state.get("step")

    text = message.lower()

    if any(word in text for word in ["cancel", "stop", "exit"]):
        request.session["chatbot_state"] = {}
        return JsonResponse({"reply": "Okay, I cancelled the current assistant flow."})

    if not mode:
        if any(
            word in text
            for word in [
                "last result",
                "last prediction",
                "recent prediction",
                "previous result",
            ]
        ):
            reply = _get_last_prediction_reply(request.user)
            return JsonResponse({"reply": reply})

        if any(
            word in text
            for word in [
                "my consultations",
                "my appointments",
                "consultation history",
                "appointments history",
                "recent consultations",
            ]
        ):
            reply = _get_consultation_summary_reply(request.user)
            return JsonResponse({"reply": reply})

        if any(word in text for word in ["appointment", "schedule", "booking", "book", "consult", "doctor"]):
            if not request.user.is_authenticated:
                reply = "To schedule an appointment, please sign in as a patient first. You can still ask general questions."
                return JsonResponse({"reply": reply})

            try:
                _ = request.user.patient
            except Exception:
                reply = "Appointments can be scheduled only for patient accounts. Please sign in as a patient."
                return JsonResponse({"reply": reply})

            state = {"mode": "booking", "step": "ask_specialization"}
            request.session["chatbot_state"] = state

            reply = "Great, I can help you schedule an appointment. What type of doctor do you want to see, like Dermatologist or Cardiologist?"
            return JsonResponse({"reply": reply})

        reply = _get_general_chatbot_reply(message, request.user)
        return JsonResponse({"reply": reply})

    if mode == "booking":
        if step == "ask_specialization":
            specialization_input = message.strip()
            matching_doctors = doctor.objects.filter(specialization__icontains=specialization_input)

            if not matching_doctors.exists():
                available = doctor.objects.values_list("specialization", flat=True).distinct()
                available_list = sorted(set([s for s in available if s]))
                if available_list:
                    options_text = ", ".join(available_list[:8])
                    reply = "I could not find any doctor with that specialization. Some available specializations are: " + options_text + "."
                else:
                    reply = "There are no doctors available in the system yet."
                return JsonResponse({"reply": reply})

            selected_doctor = matching_doctors.order_by("-rating").first()

            state["mode"] = "booking"
            state["step"] = "confirm"
            state["doctor_id"] = selected_doctor.pk
            state["specialization"] = selected_doctor.specialization
            request.session["chatbot_state"] = state

            reply = (
                "I found Dr. "
                + selected_doctor.name
                + " ("
                + selected_doctor.specialization
                + "). Do you want me to create an online consultation for today?"
            )
            return JsonResponse({"reply": reply})

        if step == "confirm":
            yes_words = ["yes", "y", "ok", "okay", "sure", "confirm", "yeah"]
            no_words = ["no", "n", "not", "later", "cancel"]

            if any(word in text for word in yes_words):
                if not request.user.is_authenticated:
                    request.session["chatbot_state"] = {}
                    reply = "Please sign in as a patient before confirming an appointment."
                    return JsonResponse({"reply": reply})

                try:
                    patient_obj = request.user.patient
                except Exception:
                    request.session["chatbot_state"] = {}
                    reply = "Appointments can be scheduled only for patient accounts. Please sign in as a patient."
                    return JsonResponse({"reply": reply})

                doctor_id = state.get("doctor_id")
                try:
                    selected_doctor = doctor.objects.get(pk=doctor_id)
                except doctor.DoesNotExist:
                    request.session["chatbot_state"] = {}
                    reply = "The selected doctor is no longer available. Please try booking again."
                    return JsonResponse({"reply": reply})

                disease = diseaseinfo(
                    patient=patient_obj,
                    diseasename="General Consultation",
                    no_of_symp=0,
                    symptomsname=[],
                    confidence=0,
                    consultdoctor=selected_doctor.specialization,
                )
                disease.save()

                consultation_new = consultation(
                    patient=patient_obj,
                    doctor=selected_doctor,
                    diseaseinfo=disease,
                    consultation_date=date.today(),
                    status="active",
                )
                consultation_new.save()

                send_appointment_notifications(consultation_new)

                request.session["patientusername"] = patient_obj.user.username
                request.session["doctorusername"] = selected_doctor.user.username
                request.session["diseaseinfo_id"] = disease.id
                request.session["consultation_id"] = consultation_new.id

                consultation_url = reverse("consultationview", args=[consultation_new.id])

                request.session["chatbot_state"] = {}

                reply = (
                    "Your appointment with Dr. "
                    + selected_doctor.name
                    + ' has been scheduled for today. You can open the consultation here: '
                    + '<a href="'
                    + consultation_url
                    + '">here</a>.'
                )
                return JsonResponse({"reply": reply})

            if any(word in text for word in no_words):
                request.session["chatbot_state"] = {}
                reply = "Okay, I did not schedule any appointment. You can start again any time."
                return JsonResponse({"reply": reply})

            reply = "Please answer with yes or no to confirm the appointment."
            return JsonResponse({"reply": reply})

    request.session["chatbot_state"] = {}
    reply = _get_general_chatbot_reply(message, request.user)
    return JsonResponse({"reply": reply})
