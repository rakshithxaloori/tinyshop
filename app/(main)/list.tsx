import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Team } from "@stackframe/stack";

export default function Shops({ teams }: { teams: Array<Team> }) {
  // TODO set selected team
  return (
    <ul
      role="list"
      className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
    >
      {teams.map((team) => (
        <Link key={team.id} href={`/${team.id}`}>
          <Card className="bg-background text-foreground p-4 rounded-lg">
            <div className="space-y-2">
              <h2 className="text-lg font-bold">{team.displayName}</h2>
              <p className="text-sm text-muted-foreground">{team.id}</p>
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>1 users</span>
                <span>2 days ago</span>
              </div>
            </div>
          </Card>
        </Link>
      ))}
    </ul>
  );
}
