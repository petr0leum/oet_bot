# -------------------------- CARD GENERATION --------------------------
oet_prompt_question = "Generate a card for speaking role play in OET exam. The card must be in JSON format with 5 keys: SETTINGS; PATIENT_CARD; DOCTOR_CARD; DOCTOR_TASK; PATIENT_TASK."
bad_card_prompt = "I don't like this card, maybe the illness is the problem or maybe the tasks just didn't turn out very well. Generate another card for speaking role play in OET exam. The card must be in JSON format with 5 keys: SETTINGS; PATIENT_CARD; DOCTOR_CARD; DOCTOR_TASK; PATIENT_TASK."
oet_cards = [
    {
        "SETTINGS" : "Local Medical Clinic",
        "PATIENT_CARD" : "You are 45 years old and recovering from a mild heart attack which you had two weeks ago. You were discharged from hospital four days ago. You are seeing the doctor because you are unsure how much physical activity is appropriate; you’re concerned it might bring on another heart attack.",
        "DOCTOR_CARD" : "You see a 45-year-old patient who suffered a mild anterior acute myocardial infarction two weeks ago. Recovery was uncomplicated and the patient was discharged from hospital four days ago. He/she is now concerned about how much physical activity is appropriate during recovery",
        "DOCTOR_TASK" : [
            "Find out reason for visit.",
            "Reassure patient about fatigue (e.g., expected: 4–6 weeks for return of full energy levels, etc.). Remind patient about heart attack recovery (e.g., gradual, lifestyle changes and medication to help, etc.). Emphasise importance of exercise (e.g., heart health: strengthening heart; overall health: lowering cholesterol; etc.).",
            "Give recommendations for exercise (moderate physical activity: patient’s recovery uncomplicated, already two weeks since hospital admission, etc.). Advise importance of joining cardiac rehabilitation programme (e.g., increasing exercise tolerance under supervision, etc.). Explore patient’s job (type of work, etc.).",
            "Give timescale for return to work (e.g., 4–6 weeks for desk job, etc.). Explain need to be physically and emotionally ready (e.g., not rushing back, planning return to work: assistance/support from employer, etc.). Explore any concerns.",
            "Provide recommendations for prevention of future attacks (diet: vegetables, whole grains; lifestyle: physically active; etc.). Reassure patient about his/her concerns (e.g., normal, appropriate, etc.)."
        ],
        "PATIENT_TASK" : [
            "When asked, say you’ve felt much weaker and very tired since the heart attack; you’re worried that any physical activity, such as walking, gardening or swimming, might bring on another heart attack.",
            "Say you’d like to know how much physical activity is advisable.",
            "When asked, say you’re an office worker. You sit at a desk all day; you don’t get much exercise at work.",
            "When asked, say you’re worried about having another heart attack so you’d like to know what you can do to reduce the risk of further attacks.",
            "Say that information has been very helpful. You’ll try to gradually do more exercise and you’ll look into the rehabilitation programme."
        ],
    },
    {
        "SETTINGS" : "Local Medical Clinic",
        "PATIENT_CARD" : "You are a 45-year-old office worker, and have been feeling tired and unwell. You think you are a bit overweight and are concerned you may have diabetes. Recent publicity about diabetes (on TV, in the newspaper) has made you decide to get a check-up.",
        "DOCTOR_CARD" : "Your patient is a 45-year-old office worker who is complaining of fatigue and feeling unwell. The patient appears to be overweight and thinks he/she may have diabetes. Recent publicity about diabetes (on TV, in the newspaper) has made him/her decide to get a check-up.",
        "DOCTOR_TASK" : [
            "Find out how patient is feeling (any symptoms, concerns, etc.).",
            "Explore patient’s lifestyle (exercise, work/life balance, etc.).",
            "Discuss possible significance of symptoms (e.g., possible underlying condition such as diabetes, etc.). Reassure patient about his/her symptoms (e.g., different possible causes, diabetes: only one possibility, can be managed, etc.).",
            "Briefly explain diabetes (e.g., type 1: insulin not produced; type 2: insulin not sufficient/effective, etc.). Outline management of diabetes (e.g., medication, diet, exercise, monitoring of blood glucose, etc.).",
            "Outline next steps (diagnostic blood test, return visit for results, consequent assessment of patient’s health and lifestyle, etc.)."
        ],
        "PATIENT_TASK" : [
            "When asked, say lately you’ve been feeling tired and unwell. Sometimes you feel dizzy, thirsty, and breathless; you also have itchy skin.",
            "Say you have a busy and stressful office job, and three teenage children, which leaves you no time for exercise. Ask if the symptoms might mean you have diabetes.",
            "Say if it is diabetes, you’d like to know how it would be treated.",
            "Say that information is helpful but you’re not sure what to do next.",
            "Say you’ll do a blood test and make an appointment to discuss the results."
        ],
    },
    {
        "SETTINGS" : "Emergency Department",
        "PATIENT_CARD" : "You are the parent of a four-year-old boy who came to the Emergency Department two hours ago, after 36 hours of recurrent vomiting and stomach pain. The doctor told you that your son had viral gastroenteritis. He was kept in for two hours on oral re-hydration fluids. Your son is not present for your discussion with the doctor.",
        "DOCTOR_CARD" : "The parent presented two hours ago at the Emergency Department with his/her four-year-old son. The child had a 36-hour history of recurrent vomiting and stomach pain which was diagnosed as viral gastroenteritis. He was given oral re-hydration fluids and observed for two hours. He is now ready to be discharged. The child is not present for your discussion with the parent.",
        "DOCTOR_TASK" : [
            "Confirm child is ready to be discharged. Find out about parent’s concerns.",
            "Explain viral gastroenteritis (e.g., irritation of stomach or intestines due to viral infection, etc.).",
            "Give information about how gastroenteritis is spread (e.g., contact with vomit/faeces of infected person: shaking hands, contaminated foods/objects, etc.).",
            "Resist request to keep child in hospital (e.g., oral re-hydration therapy usually effective, etc.). Advise on hydration and appropriate clear fluids (e.g., watered down unsweetened fruit juice, electrolyte drinks, etc.). Find out any other concerns.",
            "Advise when to seek medical advice (e.g., signs of severe dehydration: extreme thirst, lethargy, irritability, pale/sunken eyes, etc.)."
        ],
        "PATIENT_TASK" : [
            "When asked, say you still don’t really understand what viral gastroenteritis is.",
            "Say you don’t know how your son got viral gastroenteritis.",
            "Say your son looks very weak; you really think he needs to be kept in hospital.",
            "When asked, say you’re concerned about taking your son home; you just don’t know what to do if he starts to feel worse at home.",
            "Say you feel better about taking your son home now that you know what to look for and when to come back to the Emergency Department."
        ],
    },
    {
        "SETTINGS" : "Local Clinic",
        "PATIENT_CARD" : "You are the parent of a five-year-old boy. Your son was diagnosed with asthma a couple of days ago, after attending the Emergency Department with a severe bout of coughing, breathing difficulty and wheezing. You are attending a follow-up appointment with your son’s doctor. Your son has gone to the bathroom with your spouse and is not present for the discussion.",
        "DOCTOR_CARD" : "You see the parent of a five-year-old boy who was diagnosed with asthma a couple of days ago, after attending the Emergency Department with a severe bout of coughing, breathing difficulty and wheezing. This is a follow-up appointment. The child is not present for the discussion.",
        "DOCTOR_TASK" : [
            "Confirm reason for appointment (follow-up following asthma diagnosis). Find out how child has been since hospital visit (severity of asthma, frequency of attacks, effect of treatment, etc.).",
            "Find out further relevant details (any family history of: asthma, eczema, hay fever, etc.). Explore possible triggers of child’s asthma attacks (exposure to: cigarette smoke, dust mites, pollen; exercise; cold air; etc.).",
            "Give information about childhood asthma (chronic lung condition: tightening or narrowing of muscles in airways, swelling/inflammation, production of extra mucus; risk factors: family history of hay fever; etc.). Find out any concerns.",
            "Reassure parent about child’s asthma (e.g., manageable, regular monitoring, support available, etc.). Describe asthma management (e.g., identifying and controlling triggers, assessing severity of symptoms, knowing how to respond in urgent situation, informing child’s school, etc.).",
            "Outline next steps (e.g., examination of child, creation of asthma action plan, discussion of treatment, organising: support, follow-up appointments, etc.). Establish parent’s willingness to bring child into room for examination."
        ],
        "PATIENT_TASK" : [
            "When asked, say your son’s asthma hasn’t been too bad. He’s had one attack since he was diagnosed at the Emergency Department. He used the inhaler and the spacer that were given to him at the hospital and it seemed to help his symptoms.",
            "When asked, say no one in your family has asthma or eczema, but you usually get mild hay fever in the summer. When asked, say no one in your house smokes, and you usually keep it really clean. You think he has attacks after he has been running about outside.",
            "When asked, say you found the diagnosis really overwhelming and you’re not sure how you’re going to be able to help him manage his asthma.",
            "Say you feel a bit more reassured about managing your son’s asthma now.",
            "Say you’ll just go and get your son so that he can be examined."
        ],
    },
    {
        "SETTINGS" : "Medical Clinic",
        "PATIENT_CARD" : "You are 86 years old and attend regular chair exercise classes as you have difficulty walking and use a walking frame. You are concerned about your lower back, as you felt some discomfort when you woke up this morning.",
        "DOCTOR_CARD" : "You see an 86-year-old patient who has limited mobility. He/she uses a walking frame, and attends regular chair exercise classes. He/she has come to see you about discomfort in his/her lower back. You suspect mild back strain.",
        "DOCTOR_TASK" : [
            "Find out reason for patient’s visit.",
            "Find out more details about problem (exact location, any pain, etc.). Explore any possible causes (injury, exercise, etc.).",
            "Give possible diagnosis of mild back strain (over-stretching of muscles/ligaments: not cause for concern, etc.). Advise on next steps (e.g., physical examination to confirm diagnosis, etc.). Recommend one week off exercise classes (e.g., not exercising when in pain, not ignoring pain, etc.).",
            "Stress importance of rest from exercise (e.g., prevention of further injury/strain, time to recover, etc.). Make further recommendations (e.g., heat pack, paracetamol/acetaminophen, etc.).",
            "Emphasise benefits of exercise classes (e.g., improved posture, maintaining muscle strength, boosting energy/mood, social interaction, etc.). Advise against overdoing exercise (e.g., awareness of own limits, etc.). Establish patient’s consent for physical examination."
        ],
        "PATIENT_TASK" : [
            "When asked, say when you got out of bed this morning, you noticed some slight discomfort in your back; you’re concerned you might have damaged it.",
            "When asked, say the problem is in your lower back. You aren’t really in any pain; it’s more discomfort. When asked, say you haven’t had any injuries. You went to your regular chair exercise class yesterday, but nothing happened during the class. You only noticed it when you got out of bed this morning.",
            "Say you’re not in any real pain so you don’t think it’s necessary to miss a week of classes.",
            "Say now you’re wondering if exercise classes are right for you; perhaps you should just give them up.",
            "Say you’ll follow that advice; you’re okay to start the examination."
        ],
    },
    {
        "SETTINGS" : "Medical ward in a hospital",
        "PATIENT_CARD" : "You are 54 years old and you were admitted to hospital 2 days ago with pneumonia. Your symptoms have improved with intravenous antibiotics and you are due to go home. Your doctor has come to advise about going home.",
        "DOCTOR_CARD" : "You are a medical doctor working in an inpatient ward. Your patient is 54 years old and was admitted 2 days ago with right lower lobe pneumonia. They have made significant improvement with intravenous antibiotics and the decision was made by the team to discharge home with a further 3 days of oral antibiotics from today.",
        "DOCTOR_TASK" : [
            "Explain that the intravenous antibiotics have treate the pneumonia; the blood tests and vital signs are all reassuring and the plan is for discharge today with tablet antibiotics for another 3 days.",
            "Ask about their home and work situation and recommend a medical certificate for a further week off work.",
            "Advise them to return to hospital if they are not feeling better after 1 week, or sooner if they have worrying symptoms (e.g. chest pain, acute shortness of breath, high fever.",
            "Inform that they will need a chest x-ray in 6 weeks to ensure full resolution of the xray findings.",
            "Explain that the xray is very important to rule out the small possibility of serious underiying disease, for example cancer. Reassure that appointments for x-rays can be flexible around working hours."
        ],
        "PATIENT_TASK" : [
            "Explain that you are very worried about going home as you still don’t feel back to normal",
            "Say that you live with your partner and 2 teenage children and you work in a busy retail job, askif you will need more time off work.",
            "Be reluctant to take time off due to finances",
            "Ask if there is anything you need to look out for once you are at home",
            "State that you do not want to take more time off work for a chest x-ray your symptoms are better by then"
        ],
    },
] ## 510 | 414 | 455 | 571 tokens

few_shot_content = """
You are a creating AI tool that creates MEDICINE speech card for an OET role-playing exam. 
You only create tasks for roleplay in json format you have to describe 5 things: SETTINGS; PATIENT_CARD; DOCTOR_CARD; DOCTOR_TASK; PATIENT_TASK.
You make cards for general practitioners, so the illnesses should be appropriate. You write tasks for the patient and for the doctor that interact with each other.
Remember that this exam is to test English, so do not use too complicated words, write in a way that a student with English level B1 can understand.

You need to think of a place where the event takes place (write it in the SETTINGS), it should be some place where you might meet a GP.

Make up the patient's story (write it in the PATIENT_CARD) and describe it through the patient's eyes.

Now take the patient's history and rewrite it through the doctor's eyes as if it were in the medical record (write it in the DOCTOR_CARD).

Now, most importantly, come up with a task for the doctor (write it in the DOCTOR_TASK). There should be 5 tasks each for the doctor and the patient, and they should be related!
The doctor's tasks could be: Finding out the patient's complaints; What the problem is; Explaining the cause of the patient's symptoms and discomfort; Making a diagnosis and explaining it; Making an appointment for future appointments or treatment.
Be sure to write Hints for the doctor about what needs to be advised or clarified, such as: A list of things that may have caused the symptoms or illness that the doctor can clarify; A list of things to advise, rehabilitation or a change of scenery, avoiding exertion for a period of time. 

Make sure that there are exactly five tasks for doctor and patient. You can combine small tasks into one using the separator ";"

Make up an assignment for the patient (write it in PATIENT_TASK).
Write what the patient should say, answer or ask, but note that the patient's tasks should be related to the doctor's tasks. Sometimes patients show emotion and don't want to agree with the doctor's diagnosis or advice, but they eventually agree.
""" ## 500 tokens

# -------------------------- AI Patient --------------------------
ai_patient_content = """
You're a patient in a role-playing game, you have a situation card: 
'''__patient_card__ '''

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

# -------------------------- EVALUATION --------------------------
dialog_score_prompt = """
Please evaluate the following dialogue: 

__dialogue__

based on the following criteria:
    
    Linguistic Criteria:
        1. Intelligibility
            - Band 6: Pronunciation is easily understood and prosodic features (stress, intonation, rhythm) are used effectively. L1 accent has no effect on intelligibility.
            - Band 5: Easily understood. Communication is not impeded by a few pronunciation or prosodic errors and/or noticeable L1 accent. Minimal strain for the listener.
            - Band 4: Easily understood most of the time. Pronunciation or prosodic errors and/or L1 accent at times cause strain for the listener.
            - Band 3: Produces some acceptable features of spoken English. Difficult to understand because errors in pronunciation/stress/intonation and/or L1 accent cause serious strain for the listener.
            - Band 2: Often unintelligible. Frequent errors in pronunciation/stress/intonation and/or L1 accent cause severe strain for the listener.
            - Band 1: Almost entirely unintelligible.
            - Band 0: Candidate does not provide any response.

        2. Fluency
            - Band 6: Completely fluent speech at normal speed. Any hesitation is appropriate and not a sign of searching for words or structures.
            - Band 5: Fluent speech at normal speed, with only occasional repetition or self-correction. Hesitation may occasionally indicate searching for words or structures, but is generally appropriate.
            - Band 4: Uneven flow, with some repetition, especially in longer utterances. Some evidence of searching for words, which does not cause serious strain.
            - Band 3: Very uneven. Frequent pauses and repetitions indicate searching for words or structures. Excessive use of fillers and difficulty sustaining longer utterances cause serious strain for the listener.
            - Band 2: Extremely uneven. Long pauses, numerous repetitions and self-corrections make speech difficult to follow.
            - Band 1: Impossible to follow, consisting of isolated words and phrases and self-corrections, separated by long pauses.
            - Band 0: Candidate does not provide any response.

        3. Appropriateness of Language
            - Band 6: Entirely appropriate register, tone and lexis for the context. No difficulty at all in explaining technical matters in lay terms. Rich and flexible. Wide range of grammar and vocabulary used accurately and flexibly. Confident use of idiomatic speech.
            - Band 5: Mostly appropriate register, tone and lexis for the context. Occasional lapses are not intrusive. Wide range of grammar and vocabulary generally used accurately and flexibly. Occasional errors in grammar or vocabulary are not intrusive.
            - Band 4: Generally appropriate register, tone and lexis for the context, but somewhat restricted and lacking in complexity. Lapses are noticeable and at times reflect limited resources of grammar and expression. Sufficient resources to maintain the interaction. Inaccuracies in vocabulary and grammar, particularly in more complex sentences, are sometimes intrusive. Meaning is generally clear.
            - Band 3: Some evidence of appropriate register, tone and lexis, but lapses are frequent and intrusive, reflecting inadequate resources of grammar and expression. Limited vocabulary and control of grammatical structures, except very simple sentences. Persistent inaccuracies are intrusive.
            - Band 2: Mostly inappropriate register, tone and lexis for the context. Very limited resources of vocabulary and grammar, even in simple sentences. Numerous errors in word choice.
            - Band 1: Entirely inappropriate register, tone and lexis for the context. Limited in all respects.
            - Band 0: Candidate does not provide any response.

        4. Resources of Grammar and Expression
            - Band 6: Rich and flexible. Wide range of grammar and vocabulary used accurately and flexibly. Confident use of idiomatic speech.
            - Band 5: Wide range of grammar and vocabulary generally used accurately and flexibly. Occasional errors in grammar or vocabulary are not intrusive.
            - Band 4: Sufficient resources to maintain the interaction. Inaccuracies in vocabulary and grammar, particularly in more complex sentences, are sometimes intrusive. Meaning is generally clear.
            - Band 3: Limited vocabulary and control of grammatical structures, except very simple sentences. Persistent inaccuracies are intrusive.
            - Band 2: Very limited resources of vocabulary and grammar, even in simple sentences. Numerous errors in word choice.
            - Band 1: Limited in all respects.
            - Band 0: Candidate does not provide any response.

Clinical Communication Criteria: will be listed next, but the score must be between 0 and 3, where 3 is Adept use; 2 is Competent use; 1 is Partially effective use; 0 is Ineffective use:
        In the roleplay, there is evidence of the test taker …

        A. Relationship building
        - A1: Initiating the interaction appropriately (greeting, introductions, nature of interview)
        - A2: Demonstrating an attentive and respectful attitude
        - A3: Adopting a non-judgemental approach
        - A4: Showing empathy for feelings/predicament/emotional state

        B. Understanding & incorporating the patient’s perspective
        - B1: Eliciting and exploring the patient’s ideas/concerns/expectations
        - B2: Picking up the patient’s cues
        - B3: Relating explanations to elicited ideas/concerns/expectations

        C. Providing structure
        - C1: Sequencing the interview purposefully and logically
        - C2: Signposting changes in topic
        - C3: Using organising techniques in explanations

        D. Information gathering
        - D1: Facilitating the patient’s narrative with active listening techniques, minimising interruption
        - D2: Using initially open questions, appropriately moving to closed questions
        - D3: NOT using compound questions/leading questions
        - D4: Clarifying statements which are vague or need amplification
        - D5: Summarising information to encourage correction/invite further information

        E. Information giving
        - E1: Establishing initially what the patient already knows
        - E2: Pausing periodically when giving information, using the response to guide next steps
        - E3: Encouraging the patient to contribute reactions/feelings
        - E4: Checking whether the patient has understood information
        - E5: Discovering what further information the patient needs

For each criterion, provide a brief justification and your score: 
    Band number for Linguistic Criteria
    Score from 3 to 0 for Clinical Communication Criteria

And at the end, write your reasoning as to how you would rate the dialogue on a 500 point scale based on the grades given and the fact that 500 is the maximum score.
"""

only_score_prompt = "Now that you've evaluated all the criteria individually. You can rate the whole dialogue from 0 to 500. In response, write only a number"

# -------------------------- OLD --------------------------
ex_1 = """{
    Patient Card: {
        SETTINGS : Local Medical Clinic
    
        PATIENT: You are 45 years old and recovering from a mild heart attack which you had two weeks ago. You were discharged from hospital four days ago. You are seeing the doctor because you are unsure how much physical activity is appropriate; you’re concerned it might bring on another heart attack.
        
        PATIENT TASK:
        - When asked, say you’ve felt much weaker and very tired since the heart attack; you’re worried that any physical activity, such as walking, gardening or swimming, might bring on another heart attack.
        - Say you’d like to know how much physical activity is advisable.
        - When asked, say you’re an office worker. You sit at a desk all day; you don’t get much exercise at work.
        - When asked, say you’re worried about having another heart attack so you’d like to know what you can do to reduce the risk of further attacks.
        - Say that information has been very helpful. You’ll try to gradually do more exercise and you’ll look into the rehabilitation programme.
    }
    Doctor Card: {
        SETTINGS : Local Medical Clinic
        
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
        SETTINGS : Local Clinic
        
        PARENT: You are the parent of a five-year-old boy. Your son was diagnosed with asthma a couple of days ago, after attending the Emergency Department with a severe bout of coughing, breathing difficulty and wheezing. You are attending a follow-up appointment with your son’s doctor. Your son has gone to the bathroom with your spouse and is not present for the discussion.
        
        PARENT TASK:
        - When asked, say your son’s asthma hasn’t been too bad. He’s had one attack since he was diagnosed at the Emergency Department. He used the inhaler and the spacer that were given to him at the hospital and it seemed to help his symptoms.
        - When asked, say no one in your family has asthma or eczema, but you usually get mild hay fever in the summer. When asked, say no one in your house smokes, and you usually keep it really clean. You think he has attacks after he has been running about outside.
        - When asked, say you found the diagnosis really overwhelming and you’re not sure how you’re going to be able to help him manage his asthma.
        - Say you feel a bit more reassured about managing your son’s asthma now.
        - Say you’ll just go and get your son so that he can be examined.
    }
    Doctor Card: {
        SETTINGS : Local Clinic

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
        SETTINGS : Local Medical Clinic

        PATIENT: You are a 45-year-old office worker, and have been feeling tired and unwell. You think you are a bit overweight and are concerned you may have diabetes. Recent publicity about diabetes (on TV, in the newspaper) has made you decide to get a check-up.
        
        PATIENT TASK:
        - When asked, say lately you’ve been feeling tired and unwell. Sometimes you feel dizzy, thirsty, and breathless; you also have itchy skin.
        - Say you have a busy and stressful office job, and three teenage children, which leaves you no time for exercise. Ask if the symptoms might mean you have diabetes.
        - Say if it is diabetes, you’d like to know how it would be treated.
        - Say that information is helpful but you’re not sure what to do next.
        - Say you’ll do a blood test and make an appointment to discuss the results.
    }
    Doctor Card: {
        SETTINGS : Local Medical Clinic

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
        SETTINGSS: Emergency Department

        PARENT: You are the parent of a four-year-old boy who came to the Emergency Department two hours ago, after 36 hours of recurrent vomiting and stomach pain. The doctor told you that your son had viral gastroenteritis. He was kept in for two hours on oral re-hydration fluids. Your son is not present for your discussion with the doctor.

        PARENT TASK:
        - When asked, say you still don’t really understand what viral gastroenteritis is.
        - Say you don’t know how your son got viral gastroenteritis.
        - Say your son looks very weak; you really think he needs to be kept in hospital.
        - When asked, say you’re concerned about taking your son home; you just don’t know what to do if he starts to feel worse at home.
        - Say you feel better about taking your son home now that you know what to look for and when to come back to the Emergency Department.
    }
    Doctor Card: {
        SETTINGS : Emergency Department

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
        SETTINGS : Medical ward in a hospital

        PARENT: You are 54 years old and you were admitted to hospital 2 days ago with pneumonia. Your symptoms have improved with intravenous antibiotics and you are due to go home. Your doctor has come to advise about going home.

        PARENT TASK:
        - Explain that you are very worried about going home as you still don’t feel back to normal
        - Say that you live with your partner and 2 teenage children and you work in a busy retail job, askif you will need more time off work.
        - Be reluctant to take time off due to finances
        - Ask if there is anything you need to look out for once you are at home
        - State that you do not want to take more time off work for a chest x-ray your symptoms are better by then
    }
    Doctor Card: {
        SETTINGS : Medical ward in a hospital

        DOCTOR: You are a medical doctor working in an inpatient ward. Your patient is 54 years old and was admitted 2 days ago with right lower lobe pneumonia. They have made significant improvement with intravenous antibiotics and the decision was made by the team to discharge home with a further 3 days of oral antibiotics from today.

        DOCTOR TASK:
        - Explain that the intravenous antibiotics have treate the pneumonia; the blood tests and vital signs are all reassuring and the plan is for discharge today with tablet antibiotics for another 3 days
        - Ask about their home and work situation and recommend a medical certificate for a further week off work.
        - Advise them to return to hospital if they are not feeling better after 1 week, or sooner if they have worrying symptoms (e.g. chest pain, acute shortness of breath, high fever.
        - Inform that they will need a chest x-ray in 6 weeks to ensure full resolution of the xray findings
        - Explain that the xray is very important to rule out the small possibility of serious underiying disease, for example cancer. Reassure that appointments for x-rays can be flexible around working hours.
    }
}"""



old_content = f"""
You are a medicine spiking card for the OET exam creating AI tool. Don't so anything except cards creation. 
Here is an example of a card: \n{ex_1},
Here is another example of a card: \n{ex_2},
Here is another example of a card: \n{ex_3},
Here is another example of a card: \n{ex_4}

You have to come up with a SETTINGS where the event take place. 
Think of a SITUATION with which the patient came and 5 TASKS each for the PATIENT and the DOCTOR. Which includes a description of the situation, complaints and questions of a patient, and for the doctor, who should find out what the problem is, explain the causes and symptoms, make a diagnosis and prescribe treatment. 
Don't forget to write for the doctor's recommendations of what needs to be advised or clarified. A list of things that may have caused the symptoms or illness that the doctor can clarify or a list of things that could be advised. These are listed in parentheses after the description of one item in the assignment. Act on the situation, don't list it everywhere, but where relevant, write it down.
"""
### Don't forget to write for the doctor's recommendations of what needs to be advised or clarified. A list of things that may have caused the symptoms or illness that the doctor can clarify or a list of things that could be advised. These are listed in parentheses after the description of one item in the assignment.Act on the situation, don't list it everywhere, but where relevant, write it down.
### Think of what other illnesses and situations there might be and make me one task card for the patient and one for the doctor. make shure that you have exact 5 tasks for patient and a doctor.