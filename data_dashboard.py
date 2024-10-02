from copy import deepcopy
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

nutrition_df = pd.read_csv("preprocessed_nutrition_dataset.csv")

st.write("""
# Macronutrients On Energy Content - Dashboard
""")

def generate_radar_chart(nutritions: list = ['Fat_g', 'Protein_g', 'Carb_g']):
    five_most_energitic_food_groups = nutrition_df.groupby("FoodGroup").mean('Energy_kcal')['Energy_kcal'].sort_values(ascending=False)[:5].index.tolist()

    grouped_df = nutrition_df.loc[nutrition_df['FoodGroup'].isin(five_most_energitic_food_groups)]
    grouped_df = grouped_df.groupby(by='FoodGroup').mean(numeric_only=True)[nutritions]

    calculated_df_list = []

    for nutrition in nutritions:
        content_df = pd.DataFrame({
            'FoodGroup': grouped_df.index.tolist(),
            'Value': grouped_df[nutrition].values.tolist(),
        })
        nutrition_name = nutrition.split('_')
        nutrition_name = f'{nutrition_name[0]} ({nutrition_name[1]})'
        content_df['Label'] = nutrition_name
        calculated_df_list.append(content_df)

    df = pd.concat(calculated_df_list, axis=0)

    # Create a radar chart using Plotly Express
    fig = px.line_polar(df, r='Value', theta='FoodGroup', color='Label', line_close=True, labels={'Label': 'Nutritions'})
    fig.update_traces(fill='toself')  # Fill the area under the line

    return fig

nutrition_columns = ['Protein_g', 'Fat_g', 'Carb_g',
        'Sugar_g', 'Fiber_g', 'VitA_g', 'VitB6_g', 'VitB12_g', 'VitC_g',
        'VitE_g', 'Folate_g', 'Niacin_g', 'Riboflavin_g', 'Thiamin_g',
        'Calcium_g', 'Copper_g', 'Iron_g', 'Magnesium_g', 'Manganese_g',
        'Phosphorus_g', 'Selenium_g', 'Zinc_g']


selected_nutritions = st.multiselect('Select desired nutritions', nutrition_columns, ['Protein_g', 'Fat_g', 'Carb_g'])


row1_col_left, row1_col_right = st.columns([.4, .6])
with row1_col_left:

    st.write("### Nutrition Distribution Amoung Food Groups")

    fig = generate_radar_chart(selected_nutritions)

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)


with row1_col_right:    

    st.write("### Average Amount of Energy in Food Groups")
    
    grouped_df = nutrition_df.groupby('FoodGroup')[['Energy_kcal']].mean().reset_index(names=['FoodGroup'])
    grouped_df.sort_values(by='Energy_kcal', ascending=False, inplace=True)

    fig = px.bar(grouped_df, x='FoodGroup', y='Energy_kcal', labels={'variable': 'Nutritions', 'value': 'Energy in Kilo-Calories'})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)


row2_col1, row2_col2, row2_col3 = st.columns([0.3, 0.3, 0.4])

with row2_col1:

    with st.container(border=True):
        option = st.selectbox("Select the nutrition value", nutrition_columns)
        st.write("### Nutrition Distribution (Histogram)")
        fig = ff.create_distplot(nutrition_df[option].values.reshape(1, -1), [option], bin_size=5)
        st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    
    with st.container(border=True):
        # st.write('### Correlation Between Energy')
        # fig = px.scatter(nutrition_df, x='Energy_kcal', y=option)
        # st.plotly_chart(fig, use_container_width=True)

        nutrition_columns_with_energy = deepcopy(nutrition_columns)
        nutrition_columns_with_energy.append('Energy_kcal')

        top_n_values = st.slider("Select the value", min_value=1, max_value=10, value=2)
        st.write(f'### Top {top_n_values} Energy Impacting Nutritions')
        top_n_correlated_nutritions = nutrition_df[nutrition_columns_with_energy].corr(numeric_only=True)[['Energy_kcal']] \
            .sort_values(by='Energy_kcal', ascending=False)[1:top_n_values+1] \
            .reset_index(names=['Nutritions'])
        fig = px.bar(top_n_correlated_nutritions, x='Nutritions', y='Energy_kcal', text='Nutritions')
        st.plotly_chart(fig, use_container_width=True)

with row2_col3:

    with st.container(border=True):
        selected_food_group = st.selectbox('Select desired food group', nutrition_df['FoodGroup'].unique().tolist())

        st.write("### Nutrition Composition")
        nutrition_columns_with_energy = deepcopy(nutrition_columns)
        nutrition_columns_with_energy.append('Energy_kcal')
        nutrition_columns_with_energy.append('FoodGroup')

        selected_df = nutrition_df[nutrition_columns_with_energy]
        selected_df['Vitamin_g'] = (selected_df['VitA_g'] + selected_df['VitB6_g'] + selected_df['VitB12_g'] 
                                    + selected_df['VitC_g'] + selected_df['VitE_g'] + (selected_df['Folate_g'] / 1000)
                                    + selected_df['Niacin_g'] + selected_df['Riboflavin_g'] + selected_df['Thiamin_g'])
        selected_df.drop(columns=['VitA_g', 'VitB6_g', 'VitB12_g', 'VitC_g', 
                                'VitE_g', 'Folate_g', 'Niacin_g', 'Riboflavin_g', 'Thiamin_g'], inplace=True)
        selected_df = selected_df.loc[selected_df['FoodGroup'] == selected_food_group].melt(id_vars=['Energy_kcal', 'FoodGroup'], var_name='Nutrition', value_name='Value')

        fig = px.pie(selected_df, values='Value', names='Nutrition')

        st.plotly_chart(fig, use_container_width=True)
