from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':7})

# html text read from the site
html_text = requests.get('https://www.imdb.com/chart/boxoffice/').text
soup = BeautifulSoup(html_text, 'lxml')

# finding code segments of the movies
movies = soup.tbody.find_all('tr')
movies.reverse()

# defining colors for genres
colors = {'Action':'#ff0000',
          'Adventure':'#ff9700',
          'Comedy':'#fffe00',
          'Fantasy':'#86f7fc',
          'Drama':'#59ff35',
          'Mystery':'#000134',
          'Thriller':'#0001ff',
          'Sci-Fi':'#8301ff',
          'Crime':'#000000',
          'Animation':'#02ff00',
          'Horror':'#ba0545',
          'Biography':'#ba0563',
          'Documentary':'#59ff67'}

mov_sale_gen = dict()

# going thru movies for titles
for movie in movies:

      # movie title
      movie_title = movie.find('td', class_ = 'titleColumn').a
      print(f'{movie_title.text}')

      # weekend & gross sales in a list
      sales = movie.find_all('td', class_ = 'ratingColumn')
      print(f'Weekend Sales: {sales[0].text.strip()}')
      print(f'Gross Sales: {sales[1].text.strip()}')

      # if gross is equal to weekend sales, its first week
      if sales[0].text.strip() == sales[1].text.strip():
            print(f'Week: 1')

      # if not, finding weeks
      else:
            weeks = movie.find('td', class_ = 'weeksColumn')
            print(f'Weeks: {weeks.text.strip()}')

      # moving to movie's webpage
      movie_url = 'https://www.imdb.com' + movie_title['href']
      html_text = requests.get(movie_url).text

      # retrieving html text
      soup = BeautifulSoup(html_text, 'lxml')

      # finding the list of genres
      genres_seg = soup.find('div', class_ = 'ipc-chip-list sc-16ede01-4 bMBIRz')
      genres = genres_seg.find_all('a')

      # dsiplaying each genre
      for genre in genres:

            print(f'{genre.text}', end=' ')

      print('\n\n')

      # shortening movie title
      movie_title = movie_title.text.split(':')[0]

      # storing data to display
      mov_sale_gen[movie_title] = [sales[0].text.strip(), genres[0].text, colors[genres[0].text]]

#to keep record of genres
genre_record = []

# iterating thru the dict
for movie, sale_gen in mov_sale_gen.items():

      # if genre is in record, label isnt defined again
      if sale_gen[1] in genre_record:
            plt.scatter(movie, sale_gen[0][1:-1], color = sale_gen[2])

      # if new genre appears, label is defined
      else:
            plt.scatter(movie, sale_gen[0][1:-1], color = sale_gen[2], label = sale_gen[1])
            genre_record.append(sale_gen[1])

# legend details
plt.legend(loc=2, prop={'size':7})

# x, y labels & title
plt.xlabel('Top 10 Movies today', fontsize = 12)
plt.ylabel('Weekend Income (US Only) (K - M Dollars)', fontsize = 12)
plt.title('Movies v Income', fontsize = 12)

plt.show()



      
      
      
