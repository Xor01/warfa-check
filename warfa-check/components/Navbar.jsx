import React from "react";
import Image from "next/image";
export default function Navbar() {
  return (
    <div className="flex flex-row justify-between">
      <div className="flex flex-column justify-start gap-5 m-2">
        <Image
          src="/images/bassamat.png"
          width={140}
          height={140}
          alt="Bassamat Logo"
          className="w-20 h-20 rounded-lg"
        />
        <Image
          src="/images/logo.png"
          width={140}
          height={140}
          alt="Bassamat Logo"
          className="w-20 h-20 rounded-lg"
        />
        <Image
          src="/images/lang.svg"
          width={140}
          height={140}
          alt="Bassamat Logo"
          className="w-20 h-20 rounded-lg"
        />
      </div>
      <a href="" className="text-2xl text-red-600 m-3 font-bold">
        Wafra-check
      </a>
    </div>
  );
}
