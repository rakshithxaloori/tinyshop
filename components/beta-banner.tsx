import { SparklesIcon } from "lucide-react"



const BetaBanner = (
  { text, email }: { text: string; email: string }
) => {


  return (
    <div className="h-fit w-full bg-gradient-to-r from-violet-600 to-indigo-600 py-sm">

      <div className="flex flex-row text-white text-center gap-0 md:gap-2 justify-center items-center px-sm md:px-md">
        <SparklesIcon className="h-fit w-fit text-white" />
        <p>
          {text}
          {" "}
          <u>{email}</u>
        </p>
      </div>
    </div>
  )
}

export default BetaBanner