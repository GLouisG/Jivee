import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
# from skimage import io
# import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import json
from decouple import config,Csv
####
def suggester(query):

  spotify_data = pd.read_pickle('spotify_data.pickle')    
#   ####

  spoty_features = pd.read_pickle('spoty_features.pickle')

  #######
  # client_id = config("CLIENT_ID")
  # client_secret= config("CLIENT_SECRET")

  #######

  auth_manager = SpotifyClientCredentials(client_id="4c1e304bc5ba4fb780d3ce00a68a55fd", client_secret='ecbafc776986435cb6800d6f05edf576')
  sp = spotipy.Spotify(auth_manager=auth_manager)
  playlist_dic = {}
  playlist_cover_art = {}
  results = sp.search(q=query, type='playlist')
  resultss = results["playlists"]["items"]
  for i in resultss:
      playlist_dic[i['name']] = i['uri'].split(':')[2]
      playlist_cover_art[i['uri'].split(':')[2]] = i['images'][0]['url']

  print(playlist_dic)

  ######

  def generate_playlist_df(playlist_name, playlist_dic, spotify_data):
      
      playlist = pd.DataFrame()

      for i, j in enumerate(sp.playlist(playlist_dic[playlist_name])['tracks']['items']):
          playlist.loc[i, 'artist'] = j['track']['artists'][0]['name']
          playlist.loc[i, 'track_name'] = j['track']['name']
          playlist.loc[i, 'track_id'] = j['track']['id']
          playlist.loc[i, 'url'] = j['track']['album']['images'][1]['url']
          playlist.loc[i, 'date_added'] = j['added_at']

      playlist['date_added'] = pd.to_datetime(playlist['date_added'])  
      
      playlist = playlist[playlist['track_id'].isin(spotify_data['track_id'].values)].sort_values('date_added',ascending = False)

      return playlist


  try:  
    playlist_df = generate_playlist_df(query, playlist_dic, spoty_features) 
  except :
    return "Error"    

  ####

  def generate_playlist_vector(spotify_features, playlist_df, weight_factor):
      
      spotify_features_playlist = spotify_features[spotify_features['track_id'].isin(playlist_df['track_id'].values)]
      spotify_features_playlist = spotify_features_playlist.merge(playlist_df[['track_id','date_added']], on = 'track_id', how = 'inner')
      
      spotify_features_nonplaylist = spotify_features[~spotify_features['track_id'].isin(playlist_df['track_id'].values)]
      
      playlist_feature_set = spotify_features_playlist.sort_values('date_added',ascending=False)
      
      
      most_recent_date = playlist_feature_set.iloc[0,-1]
      
      for ix, row in playlist_feature_set.iterrows():
          playlist_feature_set.loc[ix,'days_from_recent'] = int((most_recent_date.to_pydatetime() - row.iloc[-1].to_pydatetime()).days)
          
      
      playlist_feature_set['weight'] = playlist_feature_set['days_from_recent'].apply(lambda x: weight_factor ** (-x))
      
      playlist_feature_set_weighted = playlist_feature_set.copy()
      
      playlist_feature_set_weighted.update(playlist_feature_set_weighted.iloc[:,:-3].mul(playlist_feature_set_weighted.weight.astype(int),0))   
      
      playlist_feature_set_weighted_final = playlist_feature_set_weighted.iloc[:, :-3]
      

      
      return playlist_feature_set_weighted_final.sum(axis = 0), spotify_features_nonplaylist

  ######
  try:
   playlist_vector, nonplaylist_df = generate_playlist_vector(spoty_features, playlist_df, 1.2)
  except:
    return "Error"

  ######

  def generate_recommendation(spotify_data, playlist_vector, nonplaylist_df):

      non_playlist = spotify_data[spotify_data['track_id'].isin(nonplaylist_df['track_id'].values)]
      non_playlist['sim'] = cosine_similarity(nonplaylist_df.drop(['track_id'], axis = 1).values, playlist_vector.drop(labels = 'track_id').values.reshape(1, -1))[:,0]
      non_playlist_top15 = non_playlist.sort_values('sim',ascending = False).head(15)
      non_playlist_top15['url'] = non_playlist_top15['track_id'].apply(lambda x: sp.track(x)['album']['images'][1]['url'])
      
      return  non_playlist_top15
  ######
  top15 = generate_recommendation(spotify_data, playlist_vector, nonplaylist_df)[['track_name', 'artist_name', 'url', 'genre']] 
  print(top15)
  return json.loads(top15.to_json(orient='records'))
  ######






