import React, { useState, useRef, useEffect } from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import { Link } from "react-router-dom";
import { useSpring, animated } from "@react-spring/web";
import AccountBar from "./AccountBar";
import Links from "./Links";

function Header() {
  const navBarRef = useRef<HTMLDivElement | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [springs, api] = useSpring(() => ({
    from: { x: -window.innerWidth },
    config: { mass: 1, tension: 200, friction: 25 },
  }));

  const toggleIsOpen = () => {
    const main: HTMLElement = document.getElementById("main")!;
    const sideBar: HTMLElement = document.getElementById("sideBar")!;
    const sideBarWidth = sideBar.offsetWidth;

    // We dynamically resize the element main or the main area of the app
    if (main && sideBar) {
      const sideBarWidth = sideBar.offsetWidth; // Get actual sidebar width
      const newLeftMargin = isOpen ? "0px" : `${sideBarWidth}px`;

      // Add transition properties to main.style
      main.style.transition = "margin-left 0.3s ease-in-out"; // Customize duration & easing

      // Set the new margin with requestAnimationFrame for smoother transition
      requestAnimationFrame(() => {
        main.style.marginLeft = newLeftMargin;
      });
    }

    setIsOpen(!isOpen);

    // We swing the sideBar out
    api.start({
      from: {
        x: isOpen ? 0 : -window.innerWidth,
      },
      to: {
        x: isOpen ? -window.innerWidth : 0,
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
        <div
          className="ml-5 text-white text-2xl p-2 shadow-md rounded-md cursor-pointer hover:shadow-lg"
          onClick={toggleIsOpen}
        >
          {isOpen ? <FaTimes /> : <FaBars />}
        </div>
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
