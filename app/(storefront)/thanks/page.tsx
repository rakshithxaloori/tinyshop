import ThanksPage from "@/components/pages/thanks-page"
import { Suspense } from "react"

const ThanksDisplayPage = () => {
  return (
    <Suspense>
      <ThanksPage />
    </Suspense>
  )
}

export default ThanksDisplayPage
