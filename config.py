from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False
    )

    chat_model = "gpt-3.5-turbo-0125" # "gpt-4o" "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125"
    game_time = 5 # mins

    bot_token: str
    openai_api_token: str
    openai_proj_oet: str
    openai_org_id: str


settings = Settings()


ex_1 = """{
    Patient Card: {
        SETTING: Local Medical Clinic
    
        PATIENT: You are 45 years old and recovering from a mild heart attack which you had two weeks ago. You were discharged from hospital four days ago. You are seeing the doctor because you are unsure how much physical activity is appropriate; you’re concerned it might bring on another heart attack.
        
        PATIENT TASK:
        - When asked, say you’ve felt much weaker and very tired since the heart attack; you’re worried that any physical activity, such as walking, gardening or swimming, might bring on another heart attack.
        - Say you’d like to know how much physical activity is advisable.
        - When asked, say you’re an office worker. You sit at a desk all day; you don’t get much exercise at work.
        - When asked, say you’re worried about having another heart attack so you’d like to know what you can do to reduce the risk of further attacks.
        - Say that information has been very helpful. You’ll try to gradually do more exercise and you’ll look into the rehabilitation programme.
    }
    Doctor Card: {
        SETTING: Local Medical Clinic
        
        DOCTOR: You see a 45-year-old patient who suffered a mild anterior acute myocardial infarction two weeks ago. Recovery was uncomplicated and the patient was discharged from hospital four days ago. He/she is now concerned about how much physical activity is appropriate during recovery
        
        DOCTOR TASK:
        - Find out reason for visit.
        - Reassure patient about fatigue (e.g., expected: 4–6 weeks for return of full energy levels, etc.). Remind patient about heart attack recovery (e.g., gradual, lifestyle changes and medication to help, etc.). Emphasise importance of exercise (e.g., heart health: strengthening heart; overall health: lowering cholesterol; etc.).
        - Give recommendations for exercise (moderate physical activity: patient’s recovery uncomplicated, already two weeks since hospital admission, etc.). Advise importance of joining cardiac rehabilitation programme (e.g., increasing exercise tolerance under supervision, etc.). Explore patient’s job (type of work, etc.).
        - Give timescale for return to work (e.g., 4–6 weeks for desk job, etc.). Explain need to be physically and emotionally ready (e.g., not rushing back, planning return to work: assistance/support from employer, etc.). Explore any concerns.
        - Provide recommendations for prevention of future attacks (diet: vegetables, whole grains; lifestyle: physically active; etc.). Reassure patient about his/her concerns (e.g., normal, appropriate, etc.).
    }
}"""
ex_2 = """{
    Patient Card: {
        SETTING: Local Clinic
        
        PARENT: You are the parent of a five-year-old boy. Your son was diagnosed with asthma a couple of days ago, after attending the Emergency Department with a severe bout of coughing, breathing difficulty and wheezing. You are attending a follow-up appointment with your son’s doctor. Your son has gone to the bathroom with your spouse and is not present for the discussion.
        
        PARENT TASK:
        - When asked, say your son’s asthma hasn’t been too bad. He’s had one attack since he was diagnosed at the Emergency Department. He used the inhaler and the spacer that were given to him at the hospital and it seemed to help his symptoms.
        - When asked, say no one in your family has asthma or eczema, but you usually get mild hay fever in the summer. When asked, say no one in your house smokes, and you usually keep it really clean. You think he has attacks after he has been running about outside.
        - When asked, say you found the diagnosis really overwhelming and you’re not sure how you’re going to be able to help him manage his asthma.
        - Say you feel a bit more reassured about managing your son’s asthma now.
        - Say you’ll just go and get your son so that he can be examined.
    }
    Doctor Card: {
        SETTING: Local Clinic

        DOCTOR: You see the parent of a five-year-old boy who was diagnosed with asthma a couple of days ago, after attending the Emergency Department with a severe bout of coughing, breathing difficulty and wheezing. This is a follow-up appointment. The child is not present for the discussion.
        
        DOCTOR TASK:
        - Confirm reason for appointment (follow-up following asthma diagnosis). Find out how child has been since hospital visit (severity of asthma, frequency of attacks, effect of treatment, etc.).
        - Find out further relevant details (any family history of: asthma, eczema, hay fever, etc.). Explore possible triggers of child’s asthma attacks (exposure to: cigarette smoke, dust mites, pollen; exercise; cold air; etc.).
        - Give information about childhood asthma (chronic lung condition: tightening or narrowing of muscles in airways, swelling/inflammation, production of extra mucus; risk factors: family history of hay fever; etc.). Find out any concerns.
        - Reassure parent about child’s asthma (e.g., manageable, regular monitoring, support available, etc.). Describe asthma management (e.g., identifying and controlling triggers, assessing severity of symptoms, knowing how to respond in urgent situation, informing child’s school, etc.).
        - Outline next steps (e.g., examination of child, creation of asthma action plan, discussion of treatment, organising: support, follow-up appointments, etc.). Establish parent’s willingness to bring child into room for examination.
    }
}"""
ex_3 = """{
    Patient Card: {
        SETTING: Local Medical Clinic

        PATIENT: You are a 45-year-old office worker, and have been feeling tired and unwell. You think you are a bit overweight and are concerned you may have diabetes. Recent publicity about diabetes (on TV, in the newspaper) has made you decide to get a check-up.
        
        PATIENT TASK:
        - When asked, say lately you’ve been feeling tired and unwell. Sometimes you feel dizzy, thirsty, and breathless; you also have itchy skin.
        - Say you have a busy and stressful office job, and three teenage children, which leaves you no time for exercise. Ask if the symptoms might mean you have diabetes.
        - Say if it is diabetes, you’d like to know how it would be treated.
        - Say that information is helpful but you’re not sure what to do next.
        - Say you’ll do a blood test and make an appointment to discuss the results.
    }
    Doctor Card: {
        SETTING: Local Medical Clinic

        DOCTOR: Your patient is a 45-year-old office worker who is complaining of fatigue and feeling unwell. The patient appears to be overweight and thinks he/she may have diabetes. Recent publicity about diabetes (on TV, in the newspaper) has made him/her decide to get a check-up.
        
        DOCTOR TASK:
        - Find out how patient is feeling (any symptoms, concerns, etc.).
        - Explore patient’s lifestyle (exercise, work/life balance, etc.).
        - Discuss possible significance of symptoms (e.g., possible underlying condition such as diabetes, etc.). Reassure patient about his/her symptoms (e.g., different possible causes, diabetes: only one possibility, can be managed, etc.).
        - Briefly explain diabetes (e.g., type 1: insulin not produced; type 2: insulin not sufficient/effective, etc.). Outline management of diabetes (e.g., medication, diet, exercise, monitoring of blood glucose, etc.).
        - Outline next steps (diagnostic blood test, return visit for results, consequent assessment of patient’s health and lifestyle, etc.).
    }
}"""
ex_4 = """{
    Patient Card: {
        SETTING: Emergency Department

        PARENT: You are the parent of a four-year-old boy who came to the Emergency Department two hours ago, after 36 hours of recurrent vomiting and stomach pain. The doctor told you that your son had viral gastroenteritis. He was kept in for two hours on oral re-hydration fluids. Your son is not present for your discussion with the doctor.

        PARENT TASK:
        - When asked, say you still don’t really understand what viral gastroenteritis is.
        - Say you don’t know how your son got viral gastroenteritis.
        - Say your son looks very weak; you really think he needs to be kept in hospital.
        - When asked, say you’re concerned about taking your son home; you just don’t know what to do if he starts to feel worse at home.
        - Say you feel better about taking your son home now that you know what to look for and when to come back to the Emergency Department.
    }
    Doctor Card: {
        SETTING: Emergency Department

        DOCTOR: The parent presented two hours ago at the Emergency Department with his/her four-year-old son. The child had a 36-hour history of recurrent vomiting and stomach pain which was diagnosed as viral gastroenteritis. He was given oral re-hydration fluids and observed for two hours. He is now ready to be discharged. The child is not present for your discussion with the parent.

        DOCTOR TASK:
        - Confirm child is ready to be discharged. Find out about parent’s concerns.
        - Explain viral gastroenteritis (e.g., irritation of stomach or intestines due to viral infection, etc.).
        - Give information about how gastroenteritis is spread (e.g., contact with vomit/faeces of infected person: shaking hands, contaminated foods/objects, etc.).
        - Resist request to keep child in hospital (e.g., oral re-hydration therapy usually effective, etc.). Advise on hydration and appropriate clear fluids (e.g., watered down unsweetened fruit juice, electrolyte drinks, etc.). Find out any other concerns.
        - Advise when to seek medical advice (e.g., signs of severe dehydration: extreme thirst, lethargy, irritability, pale/sunken eyes, etc.).
    }
}"""
ex_5 = """{
    Patient Card: {
        SETTING: Medical ward in a hospital

        PARENT: You are 54 years old and you were admitted to hospital 2 days ago with pneumonia. Your symptoms have improved with intravenous antibiotics and you are due to go home. Your doctor has come to advise about going home.

        PARENT TASK:
        - Explain that you are very worried about going home as you still don’t feel back to normal
        - Say that you live with your partner and 2 teenage children and you work in a busy retail job, askif you will need more time off work.
        - Be reluctant to take time off due to finances
        - Ask if there is anything you need to look out for once you are at home
        - State that you do not want to take more time off work for a chest x-ray your symptoms are better by then
    }
    Doctor Card: {
        SETTING: Medical ward in a hospital

        DOCTOR: You are a medical doctor working in an inpatient ward. Your patient is 54 years old and was admitted 2 days ago with right lower lobe pneumonia. They have made significant improvement with intravenous antibiotics and the decision was made by the team to discharge home with a further 3 days of oral antibiotics from today.

        DOCTOR TASK:
        - Explain that the intravenous antibiotics have treate the pneumonia; the blood tests and vital signs are all reassuring and the plan is for discharge today with tablet antibiotics for another 3 days
        - Ask about their home and work situation and recommend a medical certificate for a further week off work.
        - Advise them to return to hospital if they are not feeling better after 1 week, or sooner if they have worrying symptoms (e.g. chest pain, acute shortness of breath, high fever.
        - Inform that they will need a chest x-ray in 6 weeks to ensure full resolution of the xray findings
        - Explain that the xray is very important to rule out the small possibility of serious underiying disease, for example cancer. Reassure that appointments for x-rays can be flexible around working hours.
    }
}"""

content = f"""
You are a medicine spiking card for the OET exam creating AI tool. Don't so anything except cards creation. 
Here is an example of a card: \n{ex_1},
Here is another example of a card: \n{ex_2},
Here is another example of a card: \n{ex_3},
Here is another example of a card: \n{ex_4}

You have to come up with a SETTING where the event take place. 
Think of a SITUATION with which the patient came and 5 TASKS each for the PATIENT and the DOCTOR. Which includes a description of the situation, complaints and questions of a patient, and for the doctor, who should find out what the problem is, explain the causes and symptoms, make a diagnosis and prescribe treatment. 
Don't forget to write for the doctor's recommendations of what needs to be advised or clarified. A list of things that may have caused the symptoms or illness that the doctor can clarify or a list of things that could be advised. These are listed in parentheses after the description of one item in the assignment. Act on the situation, don't list it everywhere, but where relevant, write it down.
"""
### Don't forget to write for the doctor's recommendations of what needs to be advised or clarified. A list of things that may have caused the symptoms or illness that the doctor can clarify or a list of things that could be advised. These are listed in parentheses after the description of one item in the assignment.Act on the situation, don't list it everywhere, but where relevant, write it down.
### Think of what other illnesses and situations there might be and make me one task card for the patient and one for the doctor. make shure that you have exact 5 tasks for patient and a doctor.


system_content = """
You're a patient in a role-playing game, you have a situation card: { __patient_card__ }.
Act like a real patient on an appointment. Be silly!
The user's task is to reassure you, understand your problems, ask you a lot of questions:
If you're asked something specific, answer only the question posed.
You may be asked to tell what you came with, don't answer with sentences from the task, just give a short description (take it from your card).
If they ask you something that is not on the card, come up with a short answer that fits the situation as much as possible.
If they ask you about something that is on the card, answer briefly and don't take it out on the doctor.

If you are asked if you know something about your illness, answer that you heard something somewhere, but you don't know enough and ask the doctor to tell you more, don't pretend to be a know-it-all.

If they ask you about your lifestyle, take it from the card and answer only about your lifestyle.
If they ask you your name, think of something funny and answer only your name.

Don't dump all the information at once!
Your task is to complete your tasks one by one, either until you are asked about something or until you are asked what is bothering you. 
Try not to go beyond what's on your card. If you are asked something not on your card, answer it briefly.
"""
# All you need to do is to FOLLOW the role play card.
# Your name is AI patient.
# If they ask you your name - you can make it up, but regarding the doctor's questions about your condition, answer only what is on the notes.
# Do not move on to the next question until you have received an answer to the previous one. 