
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv("sampled_data.csv")
    return data

df = load_data()

st.title("FitLife Health and Fitness Tracking Dashboard")
st.write("Explore your health and fitness data with interactive visualizations.")

st.sidebar.header("Filters")
gender_options = ["All"] + list(df['gender'].unique())
gender = st.sidebar.selectbox("Select gender" , gender_options)
age_category = st.sidebar.selectbox("Select the age category" , df['age_category'].unique())
month = st.sidebar.selectbox("Select month name " , df['month_name'].unique())

if gender == "All":
    filtered_data = df[
        (df['age_category'] == age_category) &
        (df['month_name'] == month)
    ]
else:
    filtered_data = df[
        (df['gender'] == gender) &
        (df['age_category'] == age_category) &
        (df['month_name'] == month)
    ]

def page1():
    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview", "Activity Analysis", "Heart Rate & Stress Analysis",
        "Health Condition & Fitness Level"])
    
    with tab1:
        st.header("Overview - Key Health & Fitness Metrics")
        
        avg_heart_rate = filtered_data['avg_heart_rate'].mean()
        avg_steps = filtered_data['daily_steps'].mean()
        avg_sleep = filtered_data['hours_sleep'].mean()
        avg_calories_burned = filtered_data['calories_burned'].mean()
        avg_bmi = filtered_data['bmi'].mean()

        st.metric("Average Heart Rate (bpm)", round(avg_heart_rate, 2))
        st.metric("Average Daily Steps", round(avg_steps, 2))
        st.metric("Average Sleep Hours", round(avg_sleep, 2))
        st.metric("Average Calories Burned", round(avg_calories_burned, 2))
        st.metric("Average BMI", round(avg_bmi, 2))
        
        bmi_categories = filtered_data['type_wight']
        bmi_category_counts = bmi_categories.value_counts()

        fig_bmi = px.pie(names=bmi_category_counts.index, values=bmi_category_counts.values, title="BMI Category Distribution")
        st.plotly_chart(fig_bmi)
        
        health_condition_counts = filtered_data['health_condition'].value_counts()

        fig_health = px.pie(names=health_condition_counts.index, values=health_condition_counts.values, title="Health Condition Distribution")
        st.plotly_chart(fig_health)
        
        activity_type_counts = filtered_data['activity_type'].value_counts()

        fig_activity_type = px.bar(x=activity_type_counts.index, y=activity_type_counts.values, title="activity_type Level Distribution")
        st.plotly_chart(fig_activity_type)

        st.subheader("Filtered Data Preview")
        st.write(filtered_data.head())


    with tab2:
        st.header("Activity Analysis")
        
        col1, col2, col3 = st.columns([1,1,1])
        col4, col5, col6 = st.columns([1,1,1])
        
        with col1:
            activity_stats = filtered_data.groupby('activity_type').agg(
                total_duration=('duration_minutes', 'sum')
            ).reset_index()
            fig_duration = px.histogram(activity_stats, x='activity_type', y='total_duration',
                                  title="Total Duration per Activity Type",
                                  labels={'total_duration': 'Total Duration (Minutes)', 'activity_type': 'Activity Type'},
                                  color='activity_type', barmode='group')
            st.plotly_chart(fig_duration)
            

        with col2:
            fig_calories = px.histogram(filtered_data.groupby('activity_type').agg(
                total_calories_burned=('calories_burned', 'sum')
            ).reset_index(), x='activity_type', y='total_calories_burned',
                                  title="Total Calories Burned per Activity Type",
                                  labels={'total_calories_burned': 'Total Calories Burned', 'activity_type': 'Activity Type'},
                                  color='activity_type', barmode='group')
            st.plotly_chart(fig_calories)

        with col3:
            activity_type_counts = filtered_data['activity_type'].value_counts()
            fig_activity_distribution = px.pie(names=activity_type_counts.index, values=activity_type_counts.values,
                                               title="Activity Type Distribution", color=activity_type_counts.index)
            st.plotly_chart(fig_activity_distribution)
        
        with col4:
            activity_avg_duration = filtered_data.groupby('activity_type').agg(
                avg_duration=('duration_minutes', 'mean')
            ).reset_index()
            fig_avg_duration = px.histogram(activity_avg_duration, x='activity_type', y='avg_duration',
                                      title="Average Duration per Activity Type",
                                      labels={'avg_duration': 'Average Duration (Minutes)', 'activity_type': 'Activity Type'},
                                      color='activity_type', barmode='group')
            st.plotly_chart(fig_avg_duration)

        with col5:
            activity_avg_calories = filtered_data.groupby('activity_type').agg(
                avg_calories_burned=('calories_burned', 'mean')
            ).reset_index()
            fig_avg_calories = px.histogram(activity_avg_calories, x='activity_type', y='avg_calories_burned',
                                      title="Average Calories Burned per Activity Type",
                                      labels={'avg_calories_burned': 'Average Calories Burned', 'activity_type': 'Activity Type'},
                                      color='activity_type', barmode='group')
            st.plotly_chart(fig_avg_calories)

        with col6:
            activity_gender_stats = filtered_data.groupby(['activity_type', 'gender']).agg(
                total_duration=('duration_minutes', 'sum')
            ).reset_index()
            fig_activity_gender = px.histogram(activity_gender_stats, x='activity_type', y='total_duration',
                                         color='gender', title="Activity Type by Gender",
                                         labels={'total_duration': 'Total Duration (Minutes)', 'activity_type': 'Activity Type'},
                                         barmode='group')
            st.plotly_chart(fig_activity_gender)

        with col1:
            age_duration_stats = filtered_data.groupby('age_category').agg(
                total_duration=('duration_minutes', 'sum')
            ).reset_index()
            fig_age_duration = px.histogram(age_duration_stats, x='age_category', y='total_duration',
                                      title="Duration by Age Category",
                                      labels={'total_duration': 'Total Duration (Minutes)', 'age_category': 'Age Category'},
                                      color='age_category', barmode='group')
            st.plotly_chart(fig_age_duration)

        with col2:
            age_calories_stats = filtered_data.groupby('age_category').agg(
                total_calories_burned=('calories_burned', 'sum')
            ).reset_index()
            fig_age_calories = px.histogram(age_calories_stats, x='age_category', y='total_calories_burned',
                                      title="Calories Burned by Age Category",
                                      labels={'total_calories_burned': 'Total Calories Burned', 'age_category': 'Age Category'},
                                      color='age_category', barmode='group')
            st.plotly_chart(fig_age_calories)

        with col3:
            steps_activity_stats = filtered_data.groupby('activity_type').agg(
                total_steps=('daily_steps', 'sum')
            ).reset_index()
            fig_steps_activity = px.histogram(steps_activity_stats, x='activity_type', y='total_steps',
                                        title="Total Steps by Activity Type",
                                        labels={'total_steps': 'Total Steps', 'activity_type': 'Activity Type'},
                                        color='activity_type', barmode='group')
            st.plotly_chart(fig_steps_activity)

        with col4:
            fig_stress_activity = px.histogram(filtered_data, x='stress_level', color='activity_type',barmode='group',
                                               title="Stress Level vs Activity Type",
                                               labels={'stress_level': 'Stress Level', 'activity_type': 'Activity Type'})
            st.plotly_chart(fig_stress_activity)
        

        with col5:
            hydration_distribution = filtered_data.groupby('activity_type')['hydration_level'].mean().reset_index()
            fig_hydration = px.pie(hydration_distribution, names='activity_type', values='hydration_level',
                                   title="Hydration Level Distribution by Activity Type", color='activity_type')
            st.plotly_chart(fig_hydration)

        with col6:
            resting_heart_rate_distribution = filtered_data.groupby('activity_type')['resting_heart_rate'].mean().reset_index()
            fig_rhr = px.pie(resting_heart_rate_distribution, names='activity_type', values='resting_heart_rate',
                             title="Resting Heart Rate Distribution by Activity Type", color='activity_type')
            st.plotly_chart(fig_rhr)

        with col1:
            fig_bmi = px.bar(filtered_data.groupby('activity_type').agg(
                avg_bmi=('bmi', 'mean')
            ).reset_index(), x='activity_type', y='avg_bmi',
                             title="BMI by Activity Type",
                             labels={'avg_bmi': 'Average BMI', 'activity_type': 'Activity Type'},
                             color='activity_type', barmode='group')
            st.plotly_chart(fig_bmi)

        with col2:
            intensity_distribution = filtered_data.groupby('activity_type')['intensity'].count().reset_index()
            fig_intensity = px.bar(intensity_distribution, x='activity_type', y='intensity',
                                   title="Intensity Distribution by Activity Type",
                                   labels={'intensity': 'Intensity', 'activity_type': 'Activity Type'},
                                   color='activity_type', barmode='group')
            st.plotly_chart(fig_intensity)

        with col3:
            fig_fitness_level = px.bar(filtered_data.groupby(['activity_type', 'fitness_level']).agg(
                total_duration=('duration_minutes', 'sum')
            ).reset_index(), x='activity_type', y='total_duration', color='fitness_level',
                                       title="Fitness Level by Activity Type",
                                       labels={'total_duration': 'Total Duration (Minutes)', 'activity_type': 'Activity Type'},
                                       barmode='group')
            st.plotly_chart(fig_fitness_level)

    with tab3:
        st.header("Heart Rate & Stress Analysis")
        
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        
        with col1:
            fig_rhr_dist = px.histogram(filtered_data, x='resting_heart_rate', 
                                        title="Resting Heart Rate Distribution",
                                        labels={'resting_heart_rate': 'Resting Heart Rate'},
                                        template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_rhr_dist)
    
        with col2:
            heart_rate_activity_stats = filtered_data.groupby('activity_type').agg(
                avg_heart_rate=('resting_heart_rate', 'mean')
            ).reset_index()
            fig_heart_rate_activity = px.bar(heart_rate_activity_stats, x='activity_type', y='avg_heart_rate',
                                             title="Average Heart Rate by Activity Type",
                                             labels={'avg_heart_rate': 'Average Heart Rate', 'activity_type': 'Activity Type'},
                                             color='activity_type', barmode='group', 
                                             template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_heart_rate_activity)
    
        with col3:
            fig_stress_dist = px.histogram(filtered_data, x='stress_level', 
                                           title="Stress Level Distribution",
                                           labels={'stress_level': 'Stress Level'},
                                           template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_stress_dist)
    
        with col4:
            stress_activity_stats = filtered_data.groupby('activity_type').agg(
                avg_stress_level=('stress_level', 'mean')
            ).reset_index()
            fig_stress_activity = px.bar(stress_activity_stats, x='activity_type', y='avg_stress_level',
                                         title="Average Stress Level by Activity Type",
                                         labels={'avg_stress_level': 'Average Stress Level', 'activity_type': 'Activity Type'},
                                         color='activity_type', barmode='group', 
                                         template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_stress_activity)
    
        
    
        with col6:
            stress_gender_stats = filtered_data.groupby(['gender', 'stress_level']).agg(
                count=('stress_level', 'count')
            ).reset_index()
            fig_stress_gender = px.bar(stress_gender_stats, x='gender', y='count', color='stress_level',
                                       title="Stress Level Distribution by Gender",
                                       labels={'count': 'Count', 'gender': 'Gender'},
                                       barmode='group', template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_stress_gender)
    
        with col1:
            heart_rate_gender_stats = filtered_data.groupby(['gender']).agg(
                avg_heart_rate=('resting_heart_rate', 'mean')
            ).reset_index()
            fig_heart_rate_gender = px.bar(heart_rate_gender_stats, x='gender', y='avg_heart_rate',
                                           title="Average Heart Rate by Gender",
                                           labels={'avg_heart_rate': 'Average Heart Rate', 'gender': 'Gender'},
                                           color='gender', barmode='group', template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_heart_rate_gender)
    
        with col2:
            stress_age_stats = filtered_data.groupby('age_category').agg(
                avg_stress_level=('stress_level', 'mean')
            ).reset_index()
            fig_stress_age = px.bar(stress_age_stats, x='age_category', y='avg_stress_level',
                                    title="Average Stress Level by Age Category",
                                    labels={'avg_stress_level': 'Average Stress Level', 'age_category': 'Age Category'},
                                    color='age_category', barmode='group', 
                                    template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_stress_age)
    
        with col3:
            heart_rate_age_stats = filtered_data.groupby('age_category').agg(
                avg_heart_rate=('resting_heart_rate', 'mean')
            ).reset_index()
            fig_heart_rate_age = px.bar(heart_rate_age_stats, x='age_category', y='avg_heart_rate',
                                        title="Average Heart Rate by Age Category",
                                        labels={'avg_heart_rate': 'Average Heart Rate', 'age_category': 'Age Category'},
                                        color='age_category', barmode='group', 
                                        template='plotly_dark', text_auto=True)
            st.plotly_chart(fig_heart_rate_age)
    
        

    with tab4:
        st.header("Health Condition & Fitness Level Analysis")
    
        col1, col2, col3 = st.columns(3)
    
        health_condition_colors = ['#636EFA', '#00CC96', '#AB63FA', '#FF7F0E']  
        fitness_level_colors = ['#EF553B', '#00CC96', '#636EFA']  
    
        with col1:
            health_condition_counts = filtered_data['health_condition'].value_counts()
            fig_health_condition = px.pie(names=health_condition_counts.index, values=health_condition_counts.values,
                                          title="Health Condition Distribution", color=health_condition_counts.index,
                                          color_discrete_sequence=health_condition_colors, template='plotly_dark')
            st.plotly_chart(fig_health_condition)
    
        with col2:
            fitness_level_counts = filtered_data['fitness_level'].value_counts()
            fig_fitness_level = px.pie(names=fitness_level_counts.index, values=fitness_level_counts.values,
                                        title="Fitness Level Distribution", color=fitness_level_counts.index,
                                        color_discrete_sequence=fitness_level_colors, template='plotly_dark')
            st.plotly_chart(fig_fitness_level)
    
        with col3:
            fig_stress_health_condition = px.histogram(filtered_data, x='stress_level', color='health_condition',
                                                       title="Stress Level by Health Condition",
                                                       labels={'stress_level': 'Stress Level', 'health_condition': 'Health Condition'},
                                                       template='plotly_dark', barmode='group', text_auto=True,
                                                       color_discrete_sequence=health_condition_colors)
            st.plotly_chart(fig_stress_health_condition)
    
        with col1:
            fig_bmi_health_condition = px.histogram(filtered_data, x='bmi', color='health_condition',
                                                    title="BMI by Health Condition",
                                                    labels={'bmi': 'BMI', 'health_condition': 'Health Condition'},
                                                    template='plotly_dark', barmode='group', text_auto=True,
                                                    color_discrete_sequence=health_condition_colors)
            st.plotly_chart(fig_bmi_health_condition)
    
        with col2:
            fig_duration_fitness = px.histogram(filtered_data, x='duration_minutes', color='intensity',
                                                title="Duration by Intensity",
                                                labels={'duration_minutes': 'Duration (Minutes)', 'intensity': 'Intensity'},
                                                template='plotly_dark', barmode='group', text_auto=True,
                                                color_discrete_sequence=fitness_level_colors)
            st.plotly_chart(fig_duration_fitness)
    
        with col3:
            fig_calories_fitness = px.histogram(filtered_data, x='calories_burned', color='type_wight',
                                                title="Calories Burned by type wight",
                                                labels={'calories_burned': 'Calories Burned', 'type_wight': 'type wight'},
                                                template='plotly_dark', barmode='group', text_auto=True,
                                                color_discrete_sequence=fitness_level_colors)
            st.plotly_chart(fig_calories_fitness)
    
        with col1:
            fig_steps_fitness = px.histogram(filtered_data, x='daily_steps', color='type_wight',
                                             title="Steps by type_wight",
                                             labels={'daily_steps': 'Daily Steps', 'type_wight': 'type wight'},
                                             template='plotly_dark', barmode='group', text_auto=True,
                                             color_discrete_sequence=fitness_level_colors)
            st.plotly_chart(fig_steps_fitness)
    
        with col2:
            hydration_health_condition_stats = filtered_data.groupby('health_condition')['hydration_level'].mean().reset_index()
            fig_hydration_health_condition = px.pie(hydration_health_condition_stats, names='health_condition', values='hydration_level',
                                                    title="Hydration Level by Health Condition", color='health_condition', 
                                                    color_discrete_sequence=health_condition_colors, template='plotly_dark')
            st.plotly_chart(fig_hydration_health_condition)

def page2():
    st.title("Business Insights")

    tabs = st.tabs(["Summary Statistics", "Engagement Insights", "Health & Fitness Insights"])

    with tabs[0]:
        st.header("Summary Statistics")

        total_participants = len(filtered_data['participant_id'].unique())
        st.subheader(f"Total Participants: {total_participants}")

        avg_duration = filtered_data['duration_minutes'].mean()
        st.subheader(f"Average Workout Duration: {avg_duration:.2f} minutes")

        avg_calories = filtered_data['calories_burned'].mean()
        st.subheader(f"Average Calories Burned: {avg_calories:.2f} kcal")

        avg_steps = filtered_data['daily_steps'].mean()
        st.subheader(f"Average Daily Steps: {avg_steps:.0f} steps")

        avg_hydration = filtered_data['hydration_level'].mean()
        st.subheader(f"Average Hydration Level: {avg_hydration:.2f}")

        st.write("---")

        activity_type_counts = filtered_data['activity_type'].value_counts()
        st.subheader("Most Popular Activity Type:")
        st.write(activity_type_counts.idxmax())  

        st.write("---")

    with tabs[1]:
        st.header("Engagement Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            age_category_counts = filtered_data['age_category'].value_counts()
            fig_age_category = px.pie(names=age_category_counts.index, values=age_category_counts.values,
                                      title="Age Category Distribution", color=age_category_counts.index, 
                                      template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_age_category)

        with col2:
            gender_counts = filtered_data['gender'].value_counts()
            fig_gender = px.pie(names=gender_counts.index, values=gender_counts.values,
                                title="Gender Distribution", color=gender_counts.index,
                                template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Set1)
            st.plotly_chart(fig_gender)

        with col3:
            activity_type_counts = filtered_data['activity_type'].value_counts()
            fig_activity_type = px.bar(x=activity_type_counts.index, y=activity_type_counts.values, 
                                       title="Most Popular Activity Types", labels={'x': 'Activity Type', 'y': 'Frequency'},
                                       template='plotly_dark', color=activity_type_counts.index,
                                       color_discrete_sequence=px.colors.qualitative.Set2, barmode='group')
            st.plotly_chart(fig_activity_type)

    with tabs[2]:
        st.header("Health & Fitness Insights")

        col1, col2 = st.columns(2)

        with col1:
            stress_fitness_level = filtered_data.groupby('fitness_level')['stress_level'].mean().reset_index()
            fig_stress_fitness_level = px.bar(stress_fitness_level, x='fitness_level', y='stress_level',
                                              title="Average Stress Level by Fitness Level",
                                              labels={'stress_level': 'Average Stress Level', 'fitness_level': 'Fitness Level'},
                                              template='plotly_dark', color='fitness_level',
                                              color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_stress_fitness_level)

        with col2:
            health_condition_counts = filtered_data['health_condition'].value_counts()
            fig_health_condition = px.pie(names=health_condition_counts.index, values=health_condition_counts.values,
                                          title="Health Condition Distribution", color=health_condition_counts.index,
                                          template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_health_condition)

        health_condition_calories = filtered_data.groupby('health_condition')['calories_burned'].sum().reset_index()
        fig_health_condition_calories = px.bar(health_condition_calories, x='health_condition', y='calories_burned',
                                               title="Total Calories Burned by Health Condition",
                                               labels={'calories_burned': 'Total Calories Burned', 'health_condition': 'Health Condition'},
                                               template='plotly_dark', color='health_condition',
                                               color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_health_condition_calories)

pages = {
    'Page 1': page1,
    'Page 2':page2
}
pg = st.sidebar.radio('Select Page:', pages.keys())
pages[pg]()
