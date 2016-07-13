import {logger} from './log.js'

export const logerr = (err) => {
  if (err) {
    logger.error(err)
  }
}
