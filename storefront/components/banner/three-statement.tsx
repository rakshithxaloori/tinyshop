import { cn } from "@/lib/utils"

const ThreeStatementBanner = ({
  firstStatement,
  secondStatement,
  thirdStatement,
  statementStyles
}: {
  firstStatement: string,
  secondStatement: string,
  thirdStatement: string,
  statementStyles: string[]
}
) => {
  return (
    <div className="flex flex-col max-sm:justify-start justify-center md:items-center my-lg ">
      <h2 className={cn("text-3xl font-bold",
        statementStyles[0],
      )}>{firstStatement}</h2>
      <h2 className={cn("text-3xl font-bold", statementStyles[1])}>{secondStatement}</h2>
      <h2 className={cn("text-3xl font-bold", statementStyles[2])}>{thirdStatement}</h2>
    </div>
  )
}

export default ThreeStatementBanner