import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [slides, setSlides] = useState([]);
  const [currentSlide, setCurrentSlide] = useState(1);
  const sectionRefs = useRef([]);
  const audioRef = useRef(null);

  useEffect(() => {
    fetch("/slides.json")
      .then((res) => res.json())
      .then((data) => setSlides(data));
  }, []);

  useEffect(() => {
    if (!slides.length) return;

    const playSlideAudio = (slideNumber) => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }

      const audio = new Audio(`/avatars/slide_${slideNumber}.mp3`);
      audioRef.current = audio;
      audio.play().catch((err) => {
        console.log("Audio play blocked until user interacts:", err);
      });
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = Number(entry.target.dataset.index);
            const slide = slides[index];
            if (slide) {
              setCurrentSlide(slide.slide_number);
              playSlideAudio(slide.slide_number);
            }
          }
        });
      },
      { threshold: 0.6 }
    );

    sectionRefs.current.forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => {
      observer.disconnect();
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, [slides]);

  return (
    <div className="app">
      <div className="avatar-panel">
<video
  key={currentSlide}
  autoPlay
  muted
  playsInline
  className="avatar-image"
>
  <source src={`/avatars/avatar_slide_${currentSlide}.webm`} type="video/webm" />
</video>
  <p>AI Presenter</p>
</div>
      {slides.map((slide, index) => (
        <section
          key={slide.slide_number}
          className="slide-section"
          data-index={index}
          ref={(el) => (sectionRefs.current[index] = el)}
        >
          <div className="slide-card">
            <img
              src={slide.image_path}
              alt={`Slide ${slide.slide_number}`}
              className="slide-image"
            />
            <div className="slide-text">
              <h2>Slide {slide.slide_number}</h2>
              <p>{slide.avatar_script}</p>
            </div>
          </div>
        </section>
      ))}
    </div>
  );
}

export default App;