import React, { useEffect, useState } from "react";
import { BsFacebook, BsInstagram, BsTwitter, BsYoutube } from "react-icons/bs";

export default function Footer() {
  const [showFooter, setShowFooter] = useState(false);

  // apply to copyright since they are infinite intangible assets
  const currentYear = new Date().getFullYear();

  // Check if the user has scrolled to the bottom of the page
  const handleScroll = () => {
    const isBottom =
      window.innerHeight + window.scrollY >= document.body.scrollHeight;
    setShowFooter(isBottom);
  };

  // Add scroll event listener
  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div
      id="footer"
      className={`fixed bottom-0 w-full transform transition-transform duration-500 ${
        showFooter ? "translate-y-0" : "translate-y-full"
      }`}
    >
      <footer className="h-fit bg-gradient-to-r from-cyan-900 to-teal-900 text-white rounded-none p-2">
        <div className="w-full">
          <div className="my-1 p-2">
            <a
              target="_blank"
              href="https://www.centralhealth.net/"
              aria-label="Central Health Logo"
            >
              <img
                src="/logo-large-white.png"
                alt="Central Health Logo"
                style={{
                  width: "10%",
                  height: "10%",
                  objectFit: "cover",
                }}
              />
            </a>
          </div>
          <div className="my-1 p-2 grid grid-rows-1 grid-flow-col gap-4 w-full text-sm">
            <div>
              <h3 className="font-bold">Location</h3>
              <p>
                1111 East Cesar Chavez St. <br /> Austin, TX 78702 512.978.8000
              </p>
            </div>
            <div>
              <h3 className="font-bold">Legal</h3>
              <ul>
                <li>
                  <a
                    target="_blank"
                    href="https://www.centralhealth.net/privacy-policy/"
                  >
                    Privacy Policy
                  </a>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-white my-1 p-2 w-full sm:flex sm:items-center sm:justify-between text-sm">
            <p>
              Copyright © {currentYear} Central Health. All rights reserved.
            </p>
            <div className="mt-4 flex space-x-6 sm:mt-0 sm:justify-center">
              <a
                href="https://www.facebook.com/CentralHealthTX"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Facebook"
              >
                <BsFacebook />
              </a>
              <a
                href="https://www.instagram.com/centralhealthtx/?hl=en"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Instagram"
              >
                <BsInstagram />
              </a>
              <a
                href="https://x.com/CentralHealthTX"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Twitter"
              >
                <BsTwitter />
              </a>
              <a
                href="https://www.youtube.com/channel/UCYwWV-q7M95h1l9m6jLXf5g"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="YouTube"
              >
                <BsYoutube />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
