"use server";

import { cn } from "@/lib/utils";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { TProductFAQSection } from "@/types/product";

interface FAQSectionProps {
  data: TProductFAQSection | null;
  className?: string;
}

const FAQBuilder = (props: TProductFAQSection) => {
  const { title, data: list } = props
  return (
    <div className="flex flex-col w-full h-full py-2">
      <h1 className="text-3xl font-bold text-center">{title}</h1>
      <div className="mt-lg">
        <Accordion type="single" collapsible className="w-full">
          {
            list.map((faq: any, index: number) => {
              return (
                <AccordionItem key={index} value={`faq-${index}`} className="border-2 border-primary bg-nuetral my-sm px-4 rounded">
                  <AccordionTrigger >
                    <h2 className="text-xl px-4 text-start">{faq.question}</h2>
                  </AccordionTrigger>
                  <AccordionContent>
                    <p className="px-4 text-start">{faq.answer}</p>
                  </AccordionContent>
                </AccordionItem>
              )
            })
          }
        </Accordion>
      </div>
    </div>
  )
}

const FAQSection = (props: FAQSectionProps) => {
  const {
    data,
    className
  } = props;

  if (!data || !data.data || data.data.length === 0) {
    return null;
  }

  return (
    <section id="pdp-faq-section" className={
      cn("h-full w-full my-lg", className)
    }>
      <FAQBuilder title={data.title} data={data.data} />
    </section >
  )

}

export default FAQSection