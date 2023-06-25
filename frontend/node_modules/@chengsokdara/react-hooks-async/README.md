# Asynchronous React Hooks

Write React hooks in asynchronous way

---

_Try out useWhisper a React hook for OpenAI Whisper API_

[https://github.com/chengsokdara/use-whisper](https://github.com/chengsokdara/use-whisper)

- ### Install

`npm i @chengsokdara/react-hooks-async`

`yarn add @chengsokdara/react-hooks-async`

- ### Usage

- ###### useCallbackAsync

```typescript
import { useCallbackAsync } from '@chengsokdara/react-hooks-async'

const App = () => {
  const sampleCallback = useCallbackAsync(
    // will be wrapped in try catch
    async () => {
      await promiseFunction()
    },
    // Optional: catch error
    (err) => {
      console.error(err)
    },
    // dependency list
    []
  )

  return (
    <div>
      <button onClick={() => sampleCallback()}>Fire</button>
    </div>
  )
}
```

- ###### useEffectAsync

```typescript
import { useEffectAsync } from '@chengsokdara/react-hooks-async'
import { useState } from 'react'

const App = () => {
  const [state, setState] = useState<boolean>(false)

  useEffectAsync(
    // will be wrapped in try catch
    async () => {
      const response = await callBackend()
      setState(result.data)
    },
    // Optional: cleanup function when component unmounted
    () => {
      setState(undefined)
    },
    // Optional: catch error
    (err) => {
      console.error(err)
    },
    // dependency list
    []
  )

  return (
    <div>
      <p>
        <b>State:</b> {state}
      </p>
    </div>
  )
}
```

- ###### useMemoAsync

```typescript
import { useMemoAsync } from '@chengsokdara/react-hooks-async'

const App = () => {
  const memoizedValue = useMemoAsync(
    // will be wrapped in try catch
    async () => {
      const response = await promiseFunction()
      return response + 1
    },
    // Optional: catch error
    (err) => {
      console.error(err)
    },
    // dependency list
    []
  )

  return (
    <div>
      <p>
        <b>Value:</b> {memoizedValue}
      </p>
    </div>
  )
}
```

- ### Roadmap

  - add useTransition
  - add useLayoutEffect
  - add useImperativeHandle

---

**_Contact me for web or mobile app development using React or React Native_**  
[https://chengsokdara.github.io](https://chengsokdara.github.io)
