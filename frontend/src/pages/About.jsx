import Navbar from "../components/Navbar";

function About() {
  return (
    <>
      <Navbar />

      <main className="page">
        <h1>About DeepFake Project</h1>

        <p>
          DeepFake Project is an AI-powered system
          designed to detect manipulated and
          AI-generated media.
        </p>
      </main>
    </>
  );
}

export default About;