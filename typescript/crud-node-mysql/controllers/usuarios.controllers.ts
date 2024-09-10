import { Request, Response } from 'express';
import Usuario from '../models/usuario';

export const getUsuarios = async (req: Request, res: Response) => {
  const usuarios = await Usuario.findAll();

  res.json(usuarios);
};

export const getUsuario = async (req: Request, res: Response) => {
  const { id } = req.params;
  const usuario = await Usuario.findByPk(id);

  if (usuario) {
    res.json(usuario);
  } else {
    res.status(404).json({ message: 'Usuario no encontrado.' });
  }
};

export const postUsuarios = async (req: Request, res: Response) => {
  const { body } = req;

  try {
    const existeEmail = await Usuario.findOne({
      where: {
        email: body.email,
      },
    });

    if (existeEmail) {
      return res.status(400).json({ message: 'El e-mail ya existe.' });
    }

    const usuario = await Usuario.create({
      name: body.name,
      email: body.email,
      estado: body.estado,
    });

    await usuario.save();

    res.status(200).json({
      message: 'Usuario creado correctament.',
    });
  } catch (error) {
    res.status(500).json({
      message: 'Error al crear usuario',
    });
  }
};

export const putUsuario = async (req: Request, res: Response) => {
  const { id } = req.params;
  const { body } = req;

  try {
    const usuario = await Usuario.findByPk(id);

    if (usuario) {
      await usuario.update(body);
      res.status(200).json({
        message: 'Usuario actualizado correctamente.',
      });
    } else {
      res.json({ message: 'Usuario no encontrado.' });
    }
  } catch (error) {
    res.status(500).json({
      message: 'Error al actualizar usuario',
    });
  }
};

export const deleteUsuario = async (req: Request, res: Response) => {
  const { id } = req.params;
  const usuario = await Usuario.findByPk(id);

  if (usuario) {
    //await usuario.destroy();
    await usuario.update({ estado: 0 });
    res.status(200).json({
      message: 'Usuario eliminado correctamente.',
    });
  } else {
    return res.status(404).json({
      message: 'Usuario no encontrado.',
    });
  }
};
