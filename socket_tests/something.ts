import chatListners from "./chat.listners.ts";
import { verifyJwtToken } from "../utils/helper.ts";
import { JwtPayload } from "jsonwebtoken";
// DO We need to authenticate user in some time interval??
export default function (io) {
  io.use((socket, next) => {
    try {
      const { headers } = socket.handshake;
      // const token = headers?.token || auth?.token;
      // if (!token) return next(new Error("Authentication error"));
      let user;
      try {
        const userInfo = headers['user-info']
        //console.log(JSON.parse(userInfo))

        user = JSON.parse(userInfo)
        //console.log(headers)
        /*
        user = {
          exp: 1720515665,
          iat: 1720514765,
          auth_time: 1719989802,
          jti: 'd8b3fe3a-544d-411c-ac97-6cd02b5a7495',
          iss: 'https://devauth.chatreal.ai/realms/chatreal',
          aud: 'account',
          sub: '4b0f611b-8c50-43c6-8e68-a8166e2b8aa4',
          typ: 'Bearer',
          azp: 'chatreal-web',
          session_state: 'f520b052-74de-4b58-b21c-41781e0b3d7e',
          acr: '0',
          'allowed-origins': [ '*', 'https://chatreal.ai', 'http://localhost:3000' ],
          realm_access: {
            roles: [ 'default-roles-chatreal', 'offline_access', 'uma_authorization' ]
          },
          resource_access: { account: { roles: [Array] } },
          scope: 'openid email profile',
          sid: 'f520b052-74de-4b58-b21c-41781e0b3d7e',
          email_verified: true,
          preferred_username: 'ronit.4waytechnologies@gmail.com',
          email: 'ronit.4waytechnologies@gmail.com'
        }
        */
        //verifyJwtToken(token);
        //console.log(user)
      } catch (error) {
        console.log(error);
        return next(new Error("Authentication error"));
      }

      user = {
        ...user,
        kid: user.sub,
        roles: user?.realm_access?.roles || [],
      };
      console.log(user)
      const { kid } = user;
      if (!kid) return next(new Error("Authentication error"));
      const roomName = `room-${kid}`; //Add some secret key to room name
      socket.join(roomName);
      socket.roomName = roomName;
      socket.user = user;
      return next();
    } catch (error) {
      console.log("Error from socket listener :", error);
    }
  });

  io.on("connection", (socket) => {
    chatListners(socket, io);
    console.log("user connected", socket.id);
    socket.on("disconnect", () => {
      console.log("A user disconnected", socket.id);
    });
  });
}
