import clsx from 'clsx'
import {Button as FBButton} from "flowbite-react"

export function Button({ className, ...props }: any) {
  return (
    <FBButton
      className={clsx(
        'inline-flex text-sm outline-offset-2',
        'font-semibold',
        className
      )}
      {...props}
    />
  )
}
