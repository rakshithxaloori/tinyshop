"use server";

import { cn } from "@/lib/utils";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

interface FAQSectionProps {
  product: any;
  className?: string;
}

const faqList = [
  {
    question: "What is the return policy?",
    answer: "We have a 30-day return policy. If you are not satisfied with your purchase, you can return it within 30 days of purchase."
  },
  {
    question: "How do I track my order?",
    answer: "You can track your order by logging into your account and checking the order status. You will also receive an email with the tracking information once your order has been shipped."
  },
  {
    question: "How do I contact customer service?",
    answer: "You can contact customer service by emailing us at shop@email.com or calling us at 1-800-123-4567."
  },
  {
    question: "Do you offer gift wrapping?",
    answer: "Yes, we offer gift wrapping for an additional fee. You can select the gift wrapping option at checkout."
  },
  {
    question: "Can I cancel my order?",
    answer: "You can cancel your order within 24 hours of placing it. After 24 hours, the order cannot be canceled."
  }
]

const faqSpec = {
  title: "Frequency Asked Questions",
  list: faqList
}

const FAQBuilder = ({ faqSpec }: { faqSpec: any }) => {
  const { title, list } = faqSpec
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
                    <h2 className="text-xl px-4">{faq.question}</h2>
                  </AccordionTrigger>
                  <AccordionContent>
                    <p className="px-4">{faq.answer}</p>
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
    product,
    className
  } = props;

  return (
    <section id="pdp-faq-section" className={
      cn("h-full w-full my-lg", className)
    }>
      <FAQBuilder faqSpec={faqSpec} />
    </section >
  )

}

export default FAQSection