import React, { useState } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import { Link } from "react-router-dom";
import { useSpring, animated } from "@react-spring/web";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { x: 0 },
    config: { mass: 1, tension: 200, friction: 20 },
  }))

  const toggleIsOpen = () => {
    setIsOpen(!isOpen)
    api.start({
      from: {
        x: 0,
      },
      to: {
        x: 100,
      },
    })
  }

  return (
    <div className="p-5 justify-start items-center h-fit flex bg-gradient-to-r from-cyan-500 to-blue-500">
      <Link to="#" className="ml-5 text-2xl">
        <FaIcons.FaBars style={{ color: "white" }} onClick={toggleIsOpen} />
      </Link>
        <animated.nav
          className="h-screen bg-white w-fit shadow-lg"
          style={{...springs}}
        >
          <ul className="p-5 overflow-auto">
            <li className="text-stone-500 hover:text-stone-600 p-2 my-5 h-fit w-fit shadow-md rounded-md">
              <Link to="#" onClick={toggleIsOpen}>
                <AiIcons.AiOutlineClose />
              </Link>
            </li>
          </ul>
        </animated.nav>
    </div>
  );
}

export default Navbar;
