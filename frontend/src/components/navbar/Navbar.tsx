import React, { useState } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from "react-router-dom";
import { useSpring, animated } from "@react-spring/web";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { x: -100 },
    config: { mass: 1, tension: 200, friction: 20 },
  }));

  const toggleIsOpen = () => {
    setIsOpen(!isOpen);
    api.start({
      from: {
        x: isOpen ? 0 : -100,
      },
      to: {
        x: isOpen ? -100 : -10,
      },
    });
  };

  return (
    <div>
      <div className="p-5 justify-start items-center h-fit flex bg-gradient-to-r from-cyan-500 to-blue-500">
        <Link to="#" className="ml-5 text-2xl">
          <FaIcons.FaBars style={{ color: "white" }} onClick={toggleIsOpen} />
        </Link>
      </div>
      <animated.nav
        className="h-vp bg-white w-fit shadow-lg  p-3"
        style={{ ...springs, top: '100px', left: 0 }}
      >
        <div>TEST</div>
      </animated.nav>
    </div>
  );
}

export default Navbar;