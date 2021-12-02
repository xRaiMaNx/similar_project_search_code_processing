package Server;

import java.net.*;
import java.io.*;
import java.sql.SQLException;


class ClientHandler {
    private MyServer myServer;
    private Socket socket;
    private DataInputStream in;
    private DataOutputStream out;

    private String name;

    String getName() {
        return name;
    }

    ClientHandler(MyServer myServer, Socket socket) {
        try {
            this.myServer = myServer;
            this.socket = socket;
            this.in = new DataInputStream(socket.getInputStream());
            this.out = new DataOutputStream(socket.getOutputStream());
            this.name = "";
            new Thread(() -> {
                try {
                    if (authentication())
                        readMessages();
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    closeConnection();
                }
            }).start();
        } catch (IOException e) {
            throw new RuntimeException("Problem when creating a client handler");
        }
    }

    private boolean authentication() throws IOException, SQLException, ClassNotFoundException {
        while (true) {
            String str = in.readUTF();
            if (str.startsWith("/auth ")) {
                String[] parts = str.split(" ");
                String nick = myServer.getAuthService().getNickByLoginPass(parts[1], parts[2]);
                if (nick != null) {
                    if (!myServer.isNickBusy(nick)) {
                        sendMsg("Успешная авторизация");
                        sendMsg("Ваш nickname: " + nick);
                        name = nick;
                        myServer.broadcastMsg(name + " зашел в чат");
                        myServer.subscribe(this);
                        sendMsg("/authok " + nick);
                        System.out.println(name + " залогинился");
                        return true;
                    } else {
                        sendMsg("Account already in use");
                        System.out.println(nick + " пытается зайти с нескольких аккаунтов");
                    }
                } else {
                    sendMsg("Invalid login/pass");
                }
            } else if (str.startsWith("/reg ")) {
                String[] parts = str.split(" ");
                if (myServer.getAuthService().reg(parts[1], parts[2], parts[3]))
                    sendMsg("/regok");
                else
                    sendMsg("/regfalse");
            } else if (str.startsWith("/end")) {
                System.out.println("Клиент отключился");
                return false;
            }
        }
    }

    private void readMessages() throws IOException {
        while (true) {
            String strFromClient = in.readUTF();
            strFromClient = strFromClient.trim();
            if (strFromClient.equals("/end")) {
                sendMsg("/end");
                break;
            }
            System.out.println("от " + name + ": " + strFromClient);
            if (strFromClient.startsWith("/w ")) {
                myServer.personalMsg(strFromClient, name);
                continue;
            }
            myServer.broadcastMsg(name + ": " + strFromClient);
        }
        System.out.println(name + " отключился");
        myServer.broadcastMsg(name + " вышел из чата");
    }

    void sendMsg(String msg) {
        try {
            out.writeUTF(msg);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void closeConnection() {
        myServer.unsubscribe(this);
        try {
            in.close();
            out.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}