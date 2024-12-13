import React, { useState, useRef, useEffect } from "react";
import * as FaIcons from "react-icons/fa";
import { Link } from "react-router-dom";
import { useSpring, animated } from "@react-spring/web";
import AccountBar from "./AccountBar";
import Links from "./Links";

function Header() {
  const navBarRef = useRef<HTMLDivElement | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { x: -100 },
    config: { mass: 1, tension: 200, friction: 20 },
  }));

  const toggleIsOpen = () => {
    // We dynamically resize the element main or the main area of the app
    const main: HTMLElement | null = document.getElementById("main");

    if (main) {
      const newLeftMargin = isOpen ? "0px" : "100px";
      main.style.marginLeft = newLeftMargin;
    }

    setIsOpen(!isOpen);

    // We swing the sideBar out
    api.start({
      from: {
        x: isOpen ? 0 : -100,
      },
      to: {
        x: isOpen ? -100 : 0,
      },
    });
  };

  const updateSideBarTop = (navBarHeight: number) => {
    const sideBar = document.getElementById("sideBar");
    if (sideBar) {
      sideBar.style.top = `calc(${navBarHeight}px)`;
    }
  };

  useEffect(() => {
    if (navBarRef.current) {
      const navBarHeight = navBarRef.current.offsetHeight;
      updateSideBarTop(navBarHeight);
    }
  }, [navBarRef]);

  return (
    <div>
      <div
        id="navBar"
        className="p-5 justify-start items-center h-fit flex bg-gradient-to-r from-cyan-500 to-blue-500"
        ref={navBarRef}
      >
        <Link to="#" className="ml-5 text-2xl">
          <FaIcons.FaBars style={{ color: "white" }} onClick={toggleIsOpen} />
        </Link>
      </div>
      <animated.nav
        id="sideBar"
        className="fixed h-lvh shadow-lg p-2"
        style={{ ...springs, backgroundColor: "white" }}
      >
        <Links toggleIsOpen={toggleIsOpen} />
      </animated.nav>
    </div>
  );
}

export default Header;
