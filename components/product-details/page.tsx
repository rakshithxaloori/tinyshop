
import { cn } from "@/lib/utils";
import Image from "next/image";
import { useInView } from "framer-motion"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { useRef } from "react";
import BasicHeader from "@/template/header/basic";
// import { motion, MotionConfig } from "framer-motion"
import SearchBar from "../search-bar";
import ProductVariantSection from "@/sections/product-details-page/variant";
import TabsSection from "@/sections/product-details-page/tabs";
import FAQSection from "@/sections/product-details-page/faq";
import ReviewsSection from "@/sections/product-details-page/reviews";
import RelatedSection from "@/sections/product-details-page/related";


const ProductFAQ = ({ faqs }: { faqs: any }) => {
  return (
    <Accordion type="single" collapsible className="w-full">
      <AccordionItem value="item-1">
        <AccordionTrigger>Is it accessible?</AccordionTrigger>
        <AccordionContent>
          Yes. It adheres to the WAI-ARIA design pattern.
        </AccordionContent>
      </AccordionItem>
      <AccordionItem value="item-2">
        <AccordionTrigger>Is it styled?</AccordionTrigger>
        <AccordionContent>
          Yes. It comes with default styles that matches the other
          components&apos; aesthetic.
        </AccordionContent>
      </AccordionItem>
      <AccordionItem value="item-3">
        <AccordionTrigger>Is it animated?</AccordionTrigger>
        <AccordionContent>
          Yes. It is animated by default, but you can disable it if you prefer.
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  )
}

const Box = ({ className, children }: {
  className?: string;
  children?: React.ReactNode;
}) => {
  return (
    <div className={cn("h-full w-full bg-info border-2 rounded-sm", className,)}>

      {
        children
      }
    </div>
  )
}

// const CartHeader = () => {
//   return (
//     <motion.div
//       className="flex w-full py-4 px-8 items-center justify-start gap-2 sticky top-0 left-0 z-50 bg-white"
//     >
//       <motion.section
//         id="basic-header-name"
//         whileHover={{ scale: 1.1 }}
//       >
//         <motion.h1
//           className="text-2xl bg-primary"
//           whileHover={{ scale: 1.1 }}
//         >
//           Basic Header
//         </motion.h1>
//       </motion.section>
//       <motion.section
//         id="basic-header-nav"
//         className="flex space-x-4"
//       >
//         <motion.a
//           href="#"
//           className=""
//           whileHover={{ scale: 1.1 }}
//         >
//           Shop
//         </motion.a>
//         <motion.a
//           href="#"
//           className=""
//           whileHover={{ scale: 1.1 }}
//         >
//           About
//         </motion.a>
//         <motion.a
//           href="#"
//           className=""
//           whileHover={{ scale: 1.1 }}
//         >
//           Contact
//         </motion.a>
//       </motion.section>

//     </motion.div>
//   )
// }


const ProductDetailsPage = ({
  product
}: {
  product: any;
}
) => {
  return (
    <div className="mx-lg md:mx-2xl flex flex-col flex-1 h-full">
      <ProductVariantSection product={product}
        fallbackOptions={
          {
            fallbackImage: 'https://via.placeholder.com/400x400'
          }
        }
      />
      <TabsSection product={product} config={{}} />
      <FAQSection product={product} />
      <ReviewsSection product={product} />
      <RelatedSection product={product} />
    </div>

  );
}

export default ProductDetailsPage;