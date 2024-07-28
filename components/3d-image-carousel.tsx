import Image from 'next/image';

interface Image3DCarouselProps {
  title: string;
  images: string[];
}

const Image3DCarousel = (props: Image3DCarouselProps) => {
  const { title, images } = props

  return (
    <div className="flex flex-col min-h-max bg-transparent flex items-center justify-center">
      {/* <div className='flex flex-row justify-center'>
        <h1 className="text-4xl font-bold text-center mb-8">{title}</h1>
      </div> */}
      {/* Add your 3D image carousel component here */}
      <div className="three-d-carousel-wrapper w-full">
        <div className="three-d-carousel-track">
          {
            images.map((image, index) => (
              <div key={index} className="three-d-carousel-item relative h-full">
                <Image src={image} alt="" fill className='object-fill' loading="eager" />
              </div>
            ))
          }
        </div>
      </div>
    </div>
  );
};

export default Image3DCarousel;