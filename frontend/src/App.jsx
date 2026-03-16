import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [slides, setSlides] = useState([]);
  const sectionRefs = useRef([]);

  useEffect(() => {
    fetch("/slides.json")
      .then((res) => res.json())
      .then((data) => setSlides(data));
  }, []);

  useEffect(() => {
    if (!slides.length) return;

    const synth = window.speechSynthesis;
    let currentUtterance = null;

    const speakSlide = (text) => {
      synth.cancel();
      currentUtterance = new SpeechSynthesisUtterance(text);
      currentUtterance.rate = 1;
      currentUtterance.pitch = 1;
      currentUtterance.volume = 1;
      synth.speak(currentUtterance);
    };

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const slideIndex = Number(entry.target.dataset.index);
            const slide = slides[slideIndex];
            if (slide?.avatar_script) {
              speakSlide(slide.avatar_script);
            }
          }
        });
      },
      {
        threshold: 0.6,
      }
    );

    sectionRefs.current.forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => {
      observer.disconnect();
      synth.cancel();
    };
  }, [slides]);

  return (
    <div className="app">
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