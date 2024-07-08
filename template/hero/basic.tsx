"use server";
import Image from "next/image"

const BasicHeroSection = () => {
  return (
    <div className="hero bg-base-100 min-h-screen" data-theme="retro">
      <div className="hero-content flex-col lg:flex-row-reverse ">
        <Image
          src="https://img.daisyui.com/images/stock/photo-1635805737707-575885ab0820.jpg"
          className="max-w-sm rounded-lg shadow-2xl"
          width={600}
          height={500}
          alt="Hero Image"
        />
        <div>
          <h1 className="text-5xl font-bold daisy-text-accent">Box Office News!</h1>
          <p className="py-6">
            Provident cupiditate voluptatem et in. Quaerat fugiat ut assumenda excepturi exercitationem
            quasi. In deleniti eaque aut repudiandae et a id nisi.
          </p>
          <button className="btn btn-primary">Get Started</button>
        </div>
      </div>
    </div>
  )
}

export default BasicHeroSection