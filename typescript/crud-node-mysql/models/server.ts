import express, { Application } from 'express';
import userRoutes from '../routes/usuarios.routes';

import cors from 'cors';
import db from '../database/connect';

export class Server {
  private app: Application;
  private port: string;
  private apiRoutes = {
    usuarios: '/api/users',
  };

  constructor() {
    this.app = express();
    this.port = process.env.PORT || '8000';

    this.dbConnect();
    this.middleware();
    this.routes();
  }

  async dbConnect() {
    try {
      await db.authenticate();
    } catch (error: any) {
      throw new Error(error);
    }
  }

  middleware() {
    this.app.use(cors());

    this.app.use(express.json());

    this.app.use(express.static('public'));
  }

  routes() {
    this.app.use(this.apiRoutes.usuarios, userRoutes);
  }

  listeen() {
    this.app.listen(this.port, () => {
      console.log('Server running on port: ' + this.port);
    });
  }
}
