import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">

        <Link to="/" className="logo">
          Deep<span>Fake</span>
        </Link>

        <nav className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/analyze">Analyze</Link>
          <Link to="/history">History</Link>
          <Link to="/about">About</Link>
        </nav>

        <Link to="/analyze" className="nav-button">
          Analyze Now
        </Link>

      </div>
    </header>
  );
}

export default Navbar;