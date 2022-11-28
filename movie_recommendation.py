#streamlit run movie_recommendation.py
# Dataimport
import pandas as pd
import streamlit as st
import pandas as pd

movies_raw = pd.read_csv("movies3.csv")
movies = pd.DataFrame(movies_raw)


st.set_page_config(page_title="Leo iCaprio", page_icon=":clapper:")

from PIL import Image
image = Image.open('Robot Hi.png')

st.image(image, width = 400, use_column_width="auto")

st.header("Welcome! I am Leo iCaprio.")
st.subheader("Please choose one of the following options:\n")
st.markdown("**Option A: Lucky Try - I show you randomly selected top movies.**\n")
button_1 = st.button("Go", type = "primary")


#random movie
if button_1 == True:
    # Filter columns
    movies_random = movies[
        (movies["averageRating"] >= 7.5) & (movies["numVotes"] >= 50000)
        ]

    # Random sample check
    movies_random_sample = movies_random.sample(n=5)

    # new index
    index_list_random = []
    i = 1
    for x in range(len(movies_random_sample)):
        index_list_random.append(i)
        i += 1
    recom_random_index = pd.Series(index_list_random, dtype="int64")
    movies_random_sample.set_index(recom_random_index, inplace=True)
    st.write("\n I have found the following popular movies: \n")
    st.write(movies_random_sample[["Title", "Year", "Genre", "averageRating"]].head(5))
    st.write("Not happy? Click again on the button for other top movies.")



#title search
st.write("\n\n")
st.markdown("**Option B: Title Search - Enter your favorite movie and I find movies that you will like.**")


title = (st.text_input('Please enter the movie title'))

if title != "" and title is not None:
    st.write("I found the following movie(s) for ",title, ":\n")


    # lower case
    user_input_title = title.lower()
    # input to list
    input_check = user_input_title.split(" ")
    # calculate score for title (columns 8 and 10)
    for element in input_check:
        mask = movies["Title_split"].str.contains(element, na=True)
        movies.loc[mask, "Title_split_score"] += 1

    # calculate score for original title (columns 7 and 9)
    for element in input_check:
        mask = movies["Original_Title_split"].str.contains(element, na=True)
        movies.loc[mask, "Original_Title_split_score"] += 1

    results = movies.sort_values(
        by=["Title_split_score", "Original_Title_split_score"], ascending=False
    )
    # get maximum scoring results to filter for them in the next step
    max_title_split_score = results["Title_split_score"].max()
    max_original_title_split_score = results["Title_split_score"].max()
    results_filtered = results[
        (results["Title_split_score"] == max_title_split_score)
        | (results["Original_Title_split_score"] == max_original_title_split_score)
        ]
    result2 = results_filtered.sort_values(by=["numVotes"], ascending=False)
    max_votes = result2["numVotes"].max()
    result2["numVotes_perc"] = result2["numVotes"] / max_votes
    # show only top percentile
    result3 = result2[(result2["numVotes_perc"] >= 0.4)]
    final_result = result3[
        (result3["Title_split_score"] > 0) | (result3["Original_Title_split_score"] > 0)
        ]

    # new index for final_result
    y = 1
    x = 0
    dict_final_result = {}
    for i in range(len(final_result)):
        dict_final_result[y] = final_result.iloc[x, 0]
        y = y + 1
        x = x + 1
    # keys to list
    final_result_keys = list(dict_final_result.keys())
    # list to series
    final_result_index = pd.Series(final_result_keys, dtype="int64")
    # new index
    final_result.set_index(final_result_index, inplace=True)

    # print final result
    if len(final_result) == 0:
        st.write("I am sorry, I could not find any movies")
    else:
        st.write(
            final_result[["Title", "Original Title", "Year", "Genre", "averageRating"]]
        )

    if len(final_result) > 0:

        findings_list_raw = [0]
        i=1
        for i in range(len(final_result)+1):
            findings_list_raw.append(i)
            i+=1

        findings_list = findings_list_raw[1:]


        findings = st.multiselect("Please enter the index number of your movie.\nEnter 0, if I could not find the correct movie.",findings_list, max_selections = 1)




        #new from here
        if len(findings) > 0:
            user_movie_index = int(findings[0])
            if user_movie_index == 0:
                st.write("\n\n")
                st.write("\n\n")
                st.write("\n\n")
                st.write("\n\n")
                st.write("\n\n")
                st.write("Please search again!")
            if user_movie_index > 0:
                user_movie_index_converted = dict_final_result[user_movie_index]
                movies_user_movie_filtered = movies[
                    movies["ID"] == user_movie_index_converted
                    ]
                user_movie = movies_user_movie_filtered.iloc[0, 1]
                user_movie_id = user_movie_index_converted
                user_movie_genre = movies_user_movie_filtered.iloc[0, 4]

                st.write("\n\n")
                st.write("\n\n")
                st.write("\n\n")
                st.write("\n\n")
                st.write(
                    f"\n\nIf you like {user_movie}, you should check out these movies: \n\n"
                )
                recom1 = movies[
                    (movies["Genre"] == user_movie_genre)
                    & (movies["averageRating"] >= 7)
                    & (movies["numVotes"] >= 50000)
                    & (movies["ID"] != user_movie_id)
                    ]
                recom2 = recom1.sort_values(by="averageRating", ascending=False)
                if len(recom1) > 5:
                    recom3 = recom2.sample(n=5)
                    recom4 = recom3.sort_values(by="averageRating", ascending=False)
                    # change index
                    index_list = []
                    i = 1
                    for x in range(len(recom4)):
                        index_list.append(i)
                        i += 1
                    recom4_index = pd.Series(index_list)
                    recom4.set_index(recom4_index, inplace=True)

                    st.write(recom4[["Title", "Year", "Genre", "averageRating"]])
                elif len(recom1) == 0:
                    st.write(
                        "I am sorry, I could not find any recommendation based on your search.\nPlease check out the Year/Genre search function."
                    )
                else:
                    recom4 = recom2.sort_values(by="averageRating", ascending=False)
                    # change index
                    index_list = []
                    i = 1
                    for x in range(len(recom4)):
                        index_list.append(i)
                        i += 1
                    recom4_index = pd.Series(index_list, dtype="int64")
                    recom4.set_index(recom4_index, inplace=True)
                    st.write(recom4[["Title", "Year", "Genre", "averageRating"]])




    # reset score columns:
    movies["Title_split_score"] = 0
    movies["Original_Title_split_score"] = 0
    result2["Title_split_score"] = 0
    result2["Original_Title_split_score"] = 0
    result2["numVotes_perc"] = 0


#decade and/or genre
st.write("\n\n")
st.markdown("**Option C: Genre and/or Decade - You select your favorite genre and/or decade, and I find top movies.**")

genre = st.multiselect(
    'Please select one genre',
    ["Action","Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"], max_selections = 1)

st.write("\n\n")

decade= st.multiselect(
    'Please select one decade',
    ["1970s", "1980s", "1990s", "2000s", "2010 until today"], max_selections = 1)

st.write("\n\n")

#only decade selected
if (len(decade)) > 0 and (len(genre)) == 0:
    decades = {
        "a": "1970s",
        "b": "1980s",
        "c": "1990s",
        "d": "2000s",
        "e": "2010 until today",
    }

    user_decade = decade[0]

    st.write("\n\n")
    st.write("\n\n")
    st.write("\n\nThese movies from", user_decade," are very good: \n\n")

    # filter for decade
    if user_decade == "1970s":
        movies_filtered = movies[movies["Year"].between(1970, 1979)]

    elif user_decade == "1980s":
        movies_filtered = movies[movies["Year"].between(1980, 1989)]

    elif user_decade == "1990s":
        movies_filtered = movies[movies["Year"].between(1990, 1999)]

    elif user_decade == "2000s":
        movies_filtered = movies[movies["Year"].between(2000, 2009)]

    elif user_decade == "2010 until today":
        movies_filtered = movies[movies["Year"] >= 2010]


    recom10 = movies_filtered[
        (movies_filtered["averageRating"] > 7)
        & (movies_filtered["numVotes"] >= 50000)
        ]

    # get random selection
    recom11 = recom10.sample(n=5)

    # sort by averageRating
    recom12 = recom11.sort_values(by="averageRating", ascending=False)
    # new index
    index_list_12 = []
    i = 1
    for x in range(len(recom12)):
        index_list_12.append(i)
        i += 1
    recom12_index = pd.Series(index_list_12, dtype="int64")
    recom12.set_index(recom12_index, inplace=True)

    st.write(recom12[["Title", "Year", "Genre", "averageRating"]])


#only genre selected
if (len(genre)) > 0 and (len(decade)) == 0:


        user_genre_raw = genre[0]
        user_genre = user_genre_raw.lower()
        # find top movies with that genre

        mask = movies["Genre_split"].str.contains(user_genre)
        filtered_genre = movies.loc[mask]
        recom20 = filtered_genre[
            (filtered_genre["averageRating"] > 7)
            & (filtered_genre["numVotes"] >= 50000)
            ]
        recom21 = recom20.sample(n=5)
        recom22 = recom21.sort_values(by="averageRating", ascending=False)
        # new index
        index_list_22 = []
        i = 1
        for x in range(len(recom22)):
            index_list_22.append(i)
            i += 1
        recom22_index = pd.Series(index_list_22, dtype="int64")
        recom22.set_index(recom22_index, inplace=True)
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n If you like the Genre", user_genre.capitalize(), " you should check out these movies: \n\n")
        st.write(recom22[["Title", "Year", "Genre", "averageRating"]])


#decade and genre
if (len(decade)) > 0 and (len(genre)) > 0:
    # get user input

    signal_61 = True

    if signal_61 == True:
        user_genre_raw = genre[0]
        user_genre = user_genre_raw.lower()
        # find top movies with that genre
        mask = movies["Genre_split"].str.contains(user_genre)
        filtered_genre = movies.loc[mask]

        # get decade

        user_decade_raw = decade[0]
        user_decade = user_decade_raw


        signal_55 = True

        if signal_55 == True:
            st.write("\n\n")
            st.write("\n\n")
            st.write(
                "\n\nThese movies from ", user_decade," with the genre", user_genre.capitalize(), " are very good: \n\n"
            )

            # filter for decade
            if user_decade == "1970s":
                movies_filtered = filtered_genre[
                    filtered_genre["Year"].between(1970, 1979)
                ]

            elif user_decade == "1980s":
                movies_filtered = filtered_genre[
                    filtered_genre["Year"].between(1980, 1989)
                ]

            elif user_decade == "1990s":
                movies_filtered = filtered_genre[
                    filtered_genre["Year"].between(1990, 1999)
                ]

            elif user_decade == "2000s":
                movies_filtered = filtered_genre[
                    filtered_genre["Year"].between(2000, 2009)
                ]

            elif user_decade == "2010 until today":
                movies_filtered = filtered_genre[filtered_genre["Year"] >= 2010]

            recom96 = movies_filtered[
                (movies_filtered["averageRating"] > 7)
                & (movies_filtered["numVotes"] >= 50000)
                ]
            # length recom96
            len_recom96 = len(recom96)
            # get random selection
            if len_recom96 >= 5:
                recom97 = recom96.sample(n=5)
            else:
                recom97 = recom96.sample(n=len_recom96)

            # sort by averageRating
            recom98 = recom97.sort_values(by="averageRating", ascending=False)

            # new index
            index_list_98 = []
            i = 1
            for x in range(len(recom98)):
                index_list_98.append(i)
                i += 1
            recom98_index = pd.Series(index_list_98, dtype="int64")
            recom98.set_index(recom98_index, inplace=True)

            st.write(recom98[["Title", "Year", "Genre", "averageRating"]])