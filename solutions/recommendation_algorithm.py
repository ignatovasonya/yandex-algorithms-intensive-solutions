# -*- coding: utf-8 -*-
"""
ФИНАЛЬНЫЙ ПРОЕКТ: Рекомендательная система
- Коллаборативная фильтрация (на основе оценок пользователя, синтетические пользователи)
- Контентная фильтрация (похожие фильмы по свойствам — вычисляется "на лету")
- Сохранение тепловой карты фильмов (первые 50) и графика сходства пользователя с типажами
"""

import sys
import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

# ======================================
# 0. ФУНКЦИИ ДЛЯ КОНТЕНТНОЙ ФИЛЬТРАЦИИ
# ======================================
def jaccard_similarity(list1, list2):
    set1 = set(list1) if isinstance(list1, list) else set()
    set2 = set(list2) if isinstance(list2, list) else set()
    if len(set1) == 0 and len(set2) == 0:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0.0

def euclidean_distance(row1, row2):
    return math.sqrt(
        (row1['rating_norm'] - row2['rating_norm'])**2 +
        (row1['duration_norm'] - row2['duration_norm'])**2
    )

def numeric_similarity(row1, row2):
    MAX_DIST = math.sqrt(2)
    dist = euclidean_distance(row1, row2)
    return 1 - (dist / MAX_DIST)

def combined_similarity(row1, row2, w_numeric=0.4, w_genre=0.3, w_actors=0.3):
    sim_num = numeric_similarity(row1, row2)
    sim_gen = jaccard_similarity(row1['genre_list'], row2['genre_list'])
    sim_act = jaccard_similarity(row1['actors_list'], row2['actors_list'])
    return w_numeric * sim_num + w_genre * sim_gen + w_actors * sim_act

# ======================================
# 1. ЗАГРУЗКА И ПОДГОТОВКА ДАННЫХ ДЛЯ КОНТЕНТНОЙ ФИЛЬТРАЦИИ
# ======================================
movies = pd.read_csv('IMBD.csv')
print(f"Загружено {len(movies)} фильмов")

df = movies.copy()
df['duration'] = df['duration'].astype(str).str.replace(' min', '', regex=False)
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
df['genre_list'] = df['genre'].str.split(',')

def parse_actors(cell):
    if pd.isna(cell):
        return []
    cell = cell.strip('[]')
    cell = cell.replace("'", "").replace('"', '')
    actors = [name.strip() for name in cell.split(',') if name.strip()]
    return actors
df['actors_list'] = df['stars'].apply(parse_actors)

df_clean = df.dropna(subset=['rating', 'duration']).copy()
df_clean.reset_index(drop=True, inplace=True)

min_rating = df_clean['rating'].min()
max_rating = df_clean['rating'].max()
df_clean['rating_norm'] = (df_clean['rating'] - min_rating) / (max_rating - min_rating)

min_dur = df_clean['duration'].min()
max_dur = df_clean['duration'].max()
df_clean['duration_norm'] = (df_clean['duration'] - min_dur) / (max_dur - min_dur)

# ======================================
# 2. ТЕПЛОВАЯ КАРТА ФИЛЬМОВ (первые 50) — только один раз
# ======================================
if not os.path.exists('film_heatmap.png'):
    print("Строим тепловую карту для первых 50 фильмов...")
    sample_df = df_clean.head(50).copy()
    n = len(sample_df)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        sim_matrix[i][i] = 1
        for j in range(i + 1, n):
            sim_matrix[i][j] = sim_matrix[j][i] = combined_similarity(sample_df.iloc[i], sample_df.iloc[j])
    plt.figure(figsize=(12, 10))
    sns.heatmap(sim_matrix, annot=False, xticklabels=sample_df['title'], yticklabels=sample_df['title'], cmap='coolwarm')
    plt.title('Матрица сходства первых 50 фильмов (Жаккард + Евклид)')
    plt.tight_layout()
    plt.savefig('film_heatmap.png', dpi=150)
    plt.close()
    print("Тепловая карта сохранена как film_heatmap.png\n")
else:
    print("Тепловая карта фильмов уже есть.\n")

# ======================================
# 3. ЗАГРУЗКА ДАННЫХ ДЛЯ КОЛЛАБОРАТИВНОЙ ФИЛЬТРАЦИИ (без полной матрицы)
# ======================================
ratings = pd.read_csv('synthetic_ratings.csv')
print(f"Загружено {len(ratings)} оценок от {ratings['user_id'].nunique()} пользователей")

user_item_matrix = ratings.pivot_table(
    index='user_id',
    columns='movie_name',
    values='rating'
).fillna(0)
all_movies = user_item_matrix.columns.tolist()

user_means = user_item_matrix.mean(axis=1)
centered_matrix = user_item_matrix.sub(user_means, axis=0)   # центрированные оценки синтетиков

# Получаем тип для каждого синтетического пользователя
user_type_map = ratings.groupby('user_id')['user_type'].first().to_dict()
user_types_list = [user_type_map.get(uid, 'unknown') for uid in user_item_matrix.index]

print("Матрица пользователь-фильм готова (без полной матрицы сходства)\n")

# ======================================
# 4. ФУНКЦИЯ КОЛЛАБОРАТИВНЫХ РЕКОМЕНДАЦИЙ
# ======================================
def get_collab_recommendations(user_ratings, top_k=10, top_n=5):
    # Вектор нового пользователя
    user_vector = pd.Series(index=all_movies, dtype=float).fillna(0)
    for title, rating in user_ratings.items():
        if title in user_vector.index:
            user_vector[title] = rating
        else:
            print(f"Предупреждение: фильм '{title}' не найден в датасете")

    # Центрирование
    user_mean = user_vector[user_vector > 0].mean()
    if np.isnan(user_mean):
        user_mean = 0
    user_centered = user_vector - user_mean

    # Сходство со всеми синтетиками
    sim_scores = cosine_similarity([user_centered], centered_matrix)[0]

    # Поиск топ-K похожих (для рекомендаций)
    similar_users_idx = np.argsort(sim_scores)[::-1][:top_k]
    sim_values = sim_scores[similar_users_idx]

    # Сбор кандидатов от похожих пользователей
    candidates = {}
    for idx, sim in zip(similar_users_idx, sim_values):
        user = user_item_matrix.index[idx]
        user_ratings_raw = user_item_matrix.loc[user]
        for movie, rating in user_ratings_raw[user_ratings_raw >= 4].items():
            if movie not in user_ratings and movie not in candidates:
                candidates[movie] = 0
            if movie not in user_ratings:
                candidates[movie] += rating * sim

    if not candidates:
        return [], sim_scores
    sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    return sorted_candidates[:top_n], sim_scores

# ======================================
# 5. ФУНКЦИЯ КОНТЕНТНЫХ РЕКОМЕНДАЦИЙ
# ======================================
def get_content_recommendations(movie_title, top_n=5):
    matches = df_clean[df_clean['title'].str.lower().str.contains(movie_title.lower(), na=False)]
    if len(matches) == 0:
        return None, f"Фильм '{movie_title}' не найден."
    
    if len(matches) > 1:
        print("\nНайдено несколько вариантов:")
        for i, row in enumerate(matches.itertuples(), 1):
            print(f"  {i}. {row.title}")
        print("0 — ввести название заново")
        
        while True:
            choice = input("Введите номер или точное название: ").strip()
            if choice == '0':
                return None, "Попробуйте ввести название заново."
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(matches):
                    target = matches.iloc[idx]
                    break
                else:
                    print("Неверный номер. Попробуйте ещё раз.")
                    continue
            else:
                exact = matches[matches['title'].str.lower() == choice.lower()]
                if len(exact) == 1:
                    target = exact.iloc[0]
                    break
                else:
                    print("Название не найдено среди вариантов. Попробуйте ещё раз или введите 0.")
                    continue
    else:
        target = matches.iloc[0]

    similarities = []
    for _, row in df_clean.iterrows():
        if row['title'] == target['title']:
            continue
        sim = combined_similarity(target, row, w_numeric=0.4, w_genre=0.3, w_actors=0.3)
        similarities.append((row['title'], sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return target['title'], similarities[:top_n]

# ======================================
# 6. ФУНКЦИЯ ДЛЯ ПОСТРОЕНИЯ ГРАФИКА СХОДСТВА С ТИПАМИ
# ======================================
def plot_user_type_similarity(sim_scores, user_types, save=True):
    # Группируем по типу и усредняем
    df_sim = pd.DataFrame({'user_type': user_types, 'similarity': sim_scores})
    grouped = df_sim.groupby('user_type', as_index=False)['similarity'].mean()
    grouped = grouped.sort_values('similarity', ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=grouped, x='user_type', y='similarity', hue='user_type', legend=False)
    plt.title('Сходство ваших предпочтений с профилями синтетических пользователей')
    plt.xlabel('Тип пользователя')
    plt.ylabel('Среднее косинусное сходство')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save:
        plt.savefig('user_similarity_to_types.png', dpi=150)
    plt.show()
    print("График сходства сохранён как user_similarity_to_types.png")

# ======================================
# 7. ЕСЛИ ЗАПУСКАЕМ КАК STREAMLIT ПРИЛОЖЕНИЕ
# ======================================
if 'streamlit' in sys.modules or __name__ == '__main__' and 'streamlit' in sys.modules:
    import streamlit as st

    def add_selected_movie():
        """Callback, вызываемый при выборе фильма в радиокнопке."""
        idx = st.session_state.movie_choice
        title = st.session_state.temp_matches[idx]
        rating = st.session_state.temp_rating
        st.session_state.user_ratings[title] = rating
        st.success(f"Добавлено: {title} — {rating}")
        # Очищаем временные данные
        st.session_state.temp_matches = None
        st.session_state.temp_rating = None

    st.set_page_config(page_title="Рекомендательная система", layout="wide")
    st.title("🎬 Рекомендательная система")

    # Создание вкладок
    tab1, tab2, tab3 = st.tabs(["Коллаборативная фильтрация", "Контентная фильтрация", "Тепловая карта"])
    st.session_state.temp_matches = None
    with tab1:
        st.header("Оцените несколько фильмов")
        if 'user_ratings' not in st.session_state:
            st.session_state.user_ratings = {}
        
        with st.form("collab_form"):
            movie_input = st.text_input("Название фильма")
            rating_input = st.slider("Оценка (1-5)", min_value=1, max_value=5, value=3, step=1)
            submit = st.form_submit_button("Добавить фильм")
            if submit and movie_input:
                matches = [m for m in all_movies if movie_input.lower() in m.lower()]
                if not matches:
                    st.error(f"Фильм '{movie_input}' не найден")
                elif len(matches) == 1:
                    title = matches[0]
                    st.session_state.user_ratings[title] = rating_input
                    st.success(f"Добавлено: {title} — {rating_input}")
                else:
                    st.warning("Найдено несколько фильмов. Уточните:")
                    for i, m in enumerate(matches, 1):
                        st.write(f"{i}. {m}")
                    chosen_idx = st.number_input("Введите номер фильма", min_value=1, max_value=len(matches), step=1)
        
    # Блок выбора при нескольких совпадениях
    if st.session_state.temp_matches is not None:
        st.write("Выберите нужный фильм:")
        st.radio(
            "Варианты:",
            options=range(len(st.session_state.temp_matches)),
            format_func=lambda i: st.session_state.temp_matches[i],
            key="movie_choice",
            on_change=add_selected_movie
        )

    if st.session_state.user_ratings:
        st.subheader("Ваши оценки")
        for title, rating in st.session_state.user_ratings.items():
            st.write(f"• {title}: {rating}")
        if st.button("Получить рекомендации"):
            with st.spinner("Ищем похожих пользователей..."):
                recs, sim_scores = get_collab_recommendations(st.session_state.user_ratings, top_k=10, top_n=5)
            if recs:
                st.subheader("Рекомендуемые фильмы")
                for i, (title, score) in enumerate(recs, 1):
                    st.write(f"{i}. **{title}** — прогноз: {score:.2f}")
                # График сходства
                fig = plot_user_type_similarity(sim_scores, user_types_list, save=False)
                st.pyplot(fig)
            else:
                st.warning("Не удалось найти рекомендации. Попробуйте оценить другие фильмы.")

    with tab2:
        st.header("Поиск похожих фильмов по свойствам")
        query = st.text_input("Введите название фильма")
        if st.button("Найти похожие"):
            if query:
                with st.spinner("Ищем похожие..."):
                    target, result = get_content_recommendations(query, top_n=5)
                if target is None:
                    if isinstance(result, list):
                        st.warning("Найдено несколько фильмов:")
                        for title in result:
                            st.write(f"• {title}")
                        st.info("Пожалуйста, введите более точное название.")
                    else:
                        st.error(result)
                else:
                    st.subheader(f"Фильмы, похожие на «{target}»")
                    for i, (title, sim) in enumerate(result, 1):
                        st.write(f"{i}. **{title}** (сходство: {sim:.3f})")

    with tab3:
        st.header("Матрица сходства первых 50 фильмов")
        if not os.path.exists('film_heatmap.png'):
            st.warning("Тепловая карта не найдена. Пожалуйста, запустите консольную версию для её построения.")
        else:
            st.image('film_heatmap.png', caption='Тепловая карта сходства фильмов', use_column_width=True)

    # Если запущено как Streamlit, останавливаем дальнейшее выполнение консольного кода
    sys.exit(0)

# ======================================
# 8. КОНСОЛЬНОЕ ГЛАВНОЕ МЕНЮ (если не через streamlit)
# ======================================
if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("Выберите действие:")
        print("1 — Коллаборативная фильтрация (оцените несколько фильмов)")
        print("2 — Контентная фильтрация (похожие фильмы по свойствам)")
        print("0 — Выход")
        print("="*50)
        mode = input("Ваш выбор: ").strip()

        if mode == '1':
            # ---- Коллаборативный режим ----
            print("\nОцените несколько фильмов от 1 до 5 (или введите 'стоп' для завершения).")
            user_ratings = {}
            while True:
                title = input("\nНазвание фильма: ").strip()
                if title.lower() == 'стоп':
                    break
                matching = [m for m in all_movies if title.lower() in m.lower()]
                if not matching:
                    print("Фильм не найден. Попробуйте ещё раз.")
                    continue
                if len(matching) > 1:
                    print("Найдено несколько вариантов:")
                    for i, m in enumerate(matching[:5]):
                        print(f"  {i+1}. {m}")
                    choice = input("Введите номер (или 0, чтобы ввести название заново): ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(matching):
                            title = matching[idx]
                        else:
                            continue
                    else:
                        continue
                else:
                    title = matching[0]
                try:
                    rating = float(input("Оценка (1-5): "))
                    if rating < 1 or rating > 5:
                        print("Оценка должна быть от 1 до 5.")
                        continue
                    user_ratings[title] = rating
                    print(f"Добавлено: {title} — {rating}")
                except ValueError:
                    print("Введите число.")

            if len(user_ratings) == 0:
                print("Не введено ни одной оценки. Завершаем.")
                sys.exit()

            print("\nВаши оценки:")
            for title, rating in user_ratings.items():
                print(f"  {title}: {rating}")

            print("\nИщем похожих пользователей...")
            recommendations, sim_scores = get_collab_recommendations(user_ratings, top_k=10, top_n=5)

            # График сходства с типами
            plot_user_type_similarity(sim_scores, user_types_list)

            if not recommendations:
                print("Не удалось найти рекомендации. Попробуйте оценить другие фильмы.")
            else:
                print("\nРекомендуемые фильмы (коллаборативная фильтрация):")
                for i, (title, score) in enumerate(recommendations, 1):
                    print(f"{i}. {title} — прогноз: {score:.2f}")

        elif mode == '2':
            # ---- Контентный режим ----
            title_input = input("\nВведите название фильма (для поиска похожих): ").strip()
            target, recs = get_content_recommendations(title_input, top_n=5)
            if target is None:
                print(recs)
            else:
                print(f"\nФильмы, похожие на '{target}' (по свойствам):")
                for i, (title, sim) in enumerate(recs, 1):
                    print(f"{i}. {title} (сходство: {sim:.3f})")

        else:
            print("Выход.")
            sys.exit()