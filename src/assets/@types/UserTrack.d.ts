interface UserTrack {
  id: number;
  user_id: number;
  track_id: number;
  is_favorite: number;
  played_count: number;
  position: number;
  favorited_at_sec: number; // DateTime, in seconds
  played_at_sec: number; // DateTime, in seconds
  updated_at_sec: number; // DateTime, in seconds
}
