import React from 'react';
import LeftSidebar from '../organisms/LeftSidebar';
import ApplicationBar from '../organisms/ApplicationBar';
import GivenVideoPlayer from '../organisms/GivenVideoPlayer';
import FrameDiff from '../molecules/FramesDiff';

export default function Page() {
  const [sourceVideo, setSourceVideo] = React.useState(null);
  const [targetVideo, setTargetVideo] = React.useState(null);

  return (
    <div>
      <ApplicationBar />
      <div className="h-screen grid grid-cols-6 divide-x-2 divide-gray-300">
        <div className="col-span-2 grid grid-rows-5 divide-y-2 divide-gray-300">
          <div className="m-4 row-span-2">
            <LeftSidebar sourceVideo={sourceVideo} targetVideo={targetVideo} />
          </div>
          <div className="m-4 row-span-3">
            <FrameDiff />
          </div>
        </div>
        <div className="col-span-2">
          <div className="m-4">
            <GivenVideoPlayer
              kind="source"
              alerttext="ソース動画を指定してください。"
              video={sourceVideo}
              setVideo={setSourceVideo}
            />
          </div>
        </div>
        <div className="col-span-2">
          <div className="m-4">
            <GivenVideoPlayer
              kind="target"
              alerttext="ターゲット動画を指定してください。"
              video={targetVideo}
              setVideo={setTargetVideo}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
