import streamlit as st
import pandas as pd
import base64
import time,datetime
import random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course
from videos import resume_videos,interview_videos
import plotly.graph_objects as px #to create visualisations at the admin session
import nltk
import fitz
# from scraper import get_links
from resume_analyzer import export_resume_details
nltk.download('stopwords')

class BackgroundProcess:
    def get_table_download_link(self,df,filename,text):
        
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
        return href

    def show_pdf(self,file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    def course_recommender(self,course_list):
        st.subheader("**Courses & Certificates Recommendations 🎓**")
        c = 0
        rec_course = []
        no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
        random.shuffle(course_list)
        for c_name, c_link in course_list:
            c += 1
            st.markdown(f"({c}) [{c_name}]({c_link})")
            rec_course.append(c_name)
            if c == no_of_reco:
                break
        return rec_course





#CONNECT TO DATABASE

connection = pymysql.connect(host='localhost',user='root',password='Sauban@1234',db='cv')
cursor = connection.cursor()
class SQLHandle:
    def insert_data(self,name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
        DB_table_name = 'user_data'
        print('Attempting to Insert Record')
        insert_sql = "insert into " + DB_table_name + """
        (name,email_id,resume_score,timestamp,page_no,predicted_field,user_level,actual_skills,recommended_skills,recommended_courses) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
        cursor.execute(insert_sql, rec_values)
        connection.commit()

    st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon='./Logo/logo2.png',
    )
class ResumeAnalyzer:
    def run(self):
        img = Image.open('./Logo/logo2.png')
        # img = img.resize((250,250))
        st.image(img)
        st.title("AI Resume Analyser")
        st.sidebar.markdown("# Choose User")
        activities = ["User", "Admin", "Feedback"]
        choice = st.sidebar.selectbox("Choose among the given options:", activities)
        link = '[©Developed by Mr.Dominators](https://www.linkedin.com/in/saubansamith)'
        st.sidebar.markdown(link, unsafe_allow_html=True)


        # Create the DB
        db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
        cursor.execute(db_sql)

        # Create table User Data
        DB_table_name = 'user_data'
        table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                        Name varchar(500) NOT NULL,
                        Email_ID VARCHAR(500) NOT NULL,
                        resume_score VARCHAR(8) NOT NULL,
                        Timestamp VARCHAR(50) NOT NULL,
                        Page_no VARCHAR(5) NOT NULL,
                        Predicted_Field BLOB NOT NULL,
                        User_level BLOB NOT NULL,
                        Actual_skills BLOB NOT NULL,
                        Recommended_skills BLOB NOT NULL,
                        Recommended_courses BLOB NOT NULL,
                        PRIMARY KEY (ID));
                        """
        cursor.execute(table_sql)

        # Create table Feedback
        DB_table_name = 'user_feedback'
        table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                        Name varchar(500) NOT NULL,
                        Email VARCHAR(500) NOT NULL,
                        Score VARCHAR(8) NOT NULL,
                        Comments VARCHAR(50) NOT NULL,
                        Timestamp timestamp NOT NULL,
                        PRIMARY KEY (ID));
                        """
        cursor.execute(table_sql)

        # Create table Admin
        DB_table_name = 'user_admin'
        table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                        user_name varchar(500) NOT NULL,
                        password VARCHAR(500) NOT NULL,
                        PRIMARY KEY (ID));
                        """
        cursor.execute(table_sql)

        if choice == 'User':
            st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume, and get smart recommendations</h5>''',
                        unsafe_allow_html=True)
            pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
            if pdf_file is not None:
                with st.spinner('Uploading your Resume...'):
                    time.sleep(4)
                save_image_path = './Uploaded_Resumes/'+pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                BackgroundProcess().show_pdf(save_image_path)
                resume_data=[]
                no_of_pages=export_resume_details(save_image_path)
                from resume_analyzed import name,email,phone,skills,experience_level,certifications,projects,objective,declaration,hobbies,achievements
                # name,email,phone,skills,experience_level,certifications,projects,objective,declaration,hobbies,achievements=name[0],email[0],phone[0],skills[0],experience_level[0],certifications[0],projects[0],objective[0],declaration[0],hobbies[0],achievements[0]
                if type(name) == list:
                    name = name[0]
                if type(email) == list:
                    email = email[0]
                if type(phone) == list:
                    phone = phone[0]
                if type(experience_level) == list:
                    experience_level = experience_level[0]
                if type(certifications) == list:
                    certifications = certifications[0]
                if type(projects) == list:
                    projects = projects[0]
                if type(objective) == list:
                    objective = objective[0]
                if type(declaration) == list:
                    declaration = declaration[0]
                if type(hobbies) == list:
                    hobbies = hobbies[0]
                if type(achievements) == list:
                    achievements = achievements[0]
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: '+name)
                    st.text('Email: ' + email)
                    st.text('Contact: ' + phone)
                    st.text('Resume pages: '+str(no_of_pages))
                except:
                    pass
                cand_level = ''
                # print(f'---------------------\nExperience Level: {exp_level}\n--------------------')
                exp_level=experience_level
                if exp_level=='Fresher':
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                elif exp_level=='Intermediate':
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at Intermediate level!</h4>''',unsafe_allow_html=True)
                elif exp_level=='Experienced':
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Experienced level!''',unsafe_allow_html=True)

                # st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                try:
                    keywords = st_tags(label='### Your Current Skills',
                    text='See our skills recommendation below',
                        value=skills,key = '1  ')
                except:
                    pass
                ##  keywords
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit',
                                'ml', 'python','mysql','my sql','sqlserver','sql server','sql','pandas','numpy','scikit-learn','sklearn','scikit learn','power bi','powerbi','seaborn','matplotlib','spss','smss','ssis','ms excel','excel']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                                'javascript', 'angular js', 'c#', 'flask','html', 'css', 'js']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                skills=[i.strip() for i in skills]
                # Courses recommendation
                # print(f'---------------\n{resume_data[64]}\n---------------')
                for i in skills:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        reco_field = 'Data Science'
                        st.success(" Our analysis says you are looking for Data Science Jobs.")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h4>''',unsafe_allow_html=True)
                        rec_course = BackgroundProcess().course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        # print(i.lower())
                        reco_field = 'Web Development'
                        st.success(" Our analysis says you are looking for Web Development Jobs ")
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = BackgroundProcess().course_recommender(web_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        # print(i.lower())
                        reco_field = 'Android Development'
                        st.success(" Our analysis says you are looking for Android App Development Jobs ")
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = BackgroundProcess().course_recommender(android_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        # print(i.lower())
                        reco_field = 'IOS Development'
                        st.success(" Our analysis says you are looking for IOS App Development Jobs ")
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = BackgroundProcess().course_recommender(ios_course)
                        break

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        # print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = BackgroundProcess().course_recommender(uiux_course)
                        break

                # job_links=get_links(reco_field)
                # st.markdown('''
                #                     <h4 style='text-align: left; color: #1ed760;'>
                #                     Recommended Jobs from Naukri</h4>
                                    
                #                     ''',
                #                     unsafe_allow_html=True)
                # for job in job_links:
                #     st.markdown(f'''
                #     - {job}
                #     ''')
                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                # print(objective,declaration,hobbies,projects,achievements,sep='\n')
                if objective:
                    resume_score = resume_score+20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:rgb(173, 237, 255);'>[-] Please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if declaration:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Delcaration/h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:rgb(173, 237, 255);'>[-] Please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',unsafe_allow_html=True)

                if hobbies:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:rgb(173, 237, 255);'>[-] Please add Hobbies. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if achievements:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:rgb(173, 237, 255);'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                if projects:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color:rgb(173, 237, 255);'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                        )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
                st.balloons()

                SQLHandle().insert_data(name, email, str(resume_score), timestamp,
                            str(no_of_pages), reco_field, cand_level,",".join(skills),
                            str(recommended_skills), str(rec_course))



                # Resume writing video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                st.markdown(random.choice(resume_videos),unsafe_allow_html=True)


                ## Interview Preparation Video
                st.header("**Bonus Video for Interview Tips💡**")
                st.markdown(random.choice(interview_videos),unsafe_allow_html=True)

                # connection.commit()
        elif choice=="Admin":
            ## Admin Side
            st.success('Welcome to Admin Side')
            # st.sidebar.subheader('**ID / Password Required!**')

            ad_user = st.text_input("Username")
            ad_password = st.text_input("Password", type='password')
            if st.button('Login'):
                if ad_user == 'mr' and ad_password == 'dominators':
                    st.success("Welcome Mr Dominators")
                    # Display Data
                    cursor.execute('''SELECT*FROM user_data''')
                    data = cursor.fetchall()
                    st.header("**User's Data**")
                    df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                    'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                    'Recommended Course'])
                    st.dataframe(df)
                    st.markdown(BackgroundProcess().get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                    # Admin Side Data
                    query = 'select * from user_data;'
                    plot_data = pd.read_sql(query, connection)

                    # Pie chart for predicted field recommendations
                    labels = plot_data.predicted_field.unique()
                    labels = [str(i).strip("b'") for i in labels]
                    print(labels)
                    values = plot_data.predicted_field.value_counts()
                    print(values)
                    st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                    # print(df)
                    fig = px.Figure(px.Pie(labels=labels,values=values))
                    st.plotly_chart(fig)

                    ### Pie chart for User's👨‍💻 Experienced Level
                    labels = plot_data.user_level.unique()
                    labels = [str(i).strip("b'") for i in labels]
                    values = plot_data.user_level.value_counts()
                    st.subheader("**Pie-Chart for User's Experienced Level**")
                    fig = px.Figure(px.Pie(labels=labels,values=values)).update_layout({'title':"Pie chart for User\'s👨‍💻 Experienced Level"})
                    st.plotly_chart(fig)

                    # values = plot_data.user_level.value_counts()
                    st.subheader("**Pie-Chart for User Engagement**")
                    plot_data['date']=plot_data['Timestamp'].apply(lambda x:'-'.join(x.split('_')[0].split('-')[1:]))
                    print(plot_data['date'])
                    values=plot_data.groupby(['date'])['date'].count()
                    print(values)
                    fig = px.Figure(px.Pie(labels=values.index,values=values)).update_layout({'title':"Pie chart for User👨‍💻 Engagement"})
                    st.plotly_chart(fig)


                else:
                    st.error("Wrong ID & Password Provided")
        else:
            with st.form("feedback_form"):
                name_field=st.text_input('Name')
                email_field=st.text_input('Email')
                rate_field=st.slider('Rate us From 1-5',min_value=1,max_value=5)
                comments_field=st.text_area('Comments')
                submitted = st.form_submit_button("Submit")
                if submitted:
                    print(name_field,email_field,rate_field,comments_field,sep='\n')
                    cursor.execute('Insert into user_feedback (name,email,score,comments,timestamp) values (%s,%s,%s,%s,current_timestamp)',(name_field,email_field,rate_field,comments_field))
                    connection.commit()
                    st.success('Feedback Submitted')
ResumeAnalyzer().run()
