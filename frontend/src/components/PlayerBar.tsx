import {API_BASE} from '../api/client';
import {Track} from '../types';

type Props = {
  currentTrack: Track | null;
  onEnded?: () => void;
};

export function PlayerBar({currentTrack, onEnded}: Props) {
  return (
    <footer className='player'>
      {currentTrack ? (
        <>
          <img
            className='cover'
            src={`${API_BASE}/api/tracks/${currentTrack.id}/cover`}
            onError={(e) => ((e.currentTarget.style.visibility = 'hidden'))}
          />
          <div>
            <strong>{currentTrack.title}</strong>
            <div>{currentTrack.artist || 'Unknown artist'}</div>
          </div>
          <audio controls autoPlay src={`${API_BASE}/api/tracks/${currentTrack.id}/stream`} onEnded={onEnded} />
        </>
      ) : (
        'Выберите трек для воспроизведения'
      )}
    </footer>
  );
}
